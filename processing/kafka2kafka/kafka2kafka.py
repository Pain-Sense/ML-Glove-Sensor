from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import argparse
import time
import numpy as np
import pandas as pd
import neurokit2 as nk
from datetime import datetime
import collections

BUFFER_SIZE_SAMPLES = 2000
SAMPLING_RATE = 100
PROCESS_INTERVAL_SECONDS = 5

# Using a dictionary of deques to manage buffers per deviceId
device_buffers = collections.defaultdict(lambda: {
    'ecg': collections.deque(maxlen=BUFFER_SIZE_SAMPLES),
    'bvp': collections.deque(maxlen=BUFFER_SIZE_SAMPLES),
    'gsr': collections.deque(maxlen=BUFFER_SIZE_SAMPLES),
    'timestamp': collections.deque(maxlen=BUFFER_SIZE_SAMPLES)
})

last_processed_time = {} # Stores {'deviceId': timestamp_of_last_processing}

# Kafka Setup
parser = argparse.ArgumentParser()
parser.add_argument(
    '-a', '--address', '--bootstrap-address',
    type=str, default="kafka:9092",
    help="Endereço do broker Kafka."
)
args = parser.parse_args()

producer = None
consumer = None

# Kafka connection loop
print(f"Attempting to connect to Kafka brokers at {args.address}...")
while producer is None or consumer is None:
    try:
        if producer is None:
            producer = KafkaProducer(
                bootstrap_servers=[args.address],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("KafkaProducer connected.")
        if consumer is None:
            consumer = KafkaConsumer(
                'SensorData', # Topic to consume raw sensor data from
                bootstrap_servers=[args.address],
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            print("KafkaConsumer connected.")
    except NoBrokersAvailable:
        print(f"No Kafka brokers available at {args.address}. Retrying in 5 seconds...")
        producer = None
        consumer = None
        time.sleep(5)
    except Exception as e:
        print(f"Error connecting to Kafka: {e}. Retrying in 5 seconds...")
        producer = None
        consumer = None
        time.sleep(5)

# --- Feature Extraction Functions ---

def compute_ecg_features(ecg_signal_array):
    """
    Computes Heart Rate (HR) and Heart Rate Variability (HRV) time-domain features.
    Handles potential NeuroKit warnings/errors by checking for NaN values.
    """
    # Pre-check for flat or invalid signal
    if not np.any(np.isfinite(ecg_signal_array)) or np.all(ecg_signal_array == ecg_signal_array[0]):
        return {}
    if len(ecg_signal_array) < SAMPLING_RATE * 5: # Recommended minimum 5 seconds for robust HR/HRV
        return {}

    features = {}
    try:
        ecg_signals, info = nk.ecg_process(ecg_signal_array, sampling_rate=SAMPLING_RATE)

        # 1. Heart Rate (HR)
        if "ECG_Rate" in ecg_signals.columns:
            hr_val = ecg_signals["ECG_Rate"].mean()
            if not np.isnan(hr_val):
                features['heart_rate'] = round(hr_val, 2)

        # 2. Heart Rate Variability (HRV) - Time Domain
        hrv_time_features = nk.hrv_time(ecg_signals, sampling_rate=SAMPLING_RATE, show=False)

        if not hrv_time_features.empty:
            # Check for NaN values before adding to features
            sdnn_val = hrv_time_features['HRV_SDNN'].iloc[0]
            if not np.isnan(sdnn_val):
                features['hrv_sdnn'] = round(sdnn_val, 4)

            rmssd_val = hrv_time_features['HRV_RMSSD'].iloc[0]
            if not np.isnan(rmssd_val):
                features['hrv_rmssd'] = round(rmssd_val, 4)

            pnn50_val = hrv_time_features['HRV_pNN50'].iloc[0]
            if not np.isnan(pnn50_val):
                features['hrv_pnn50'] = round(pnn50_val, 2)

        return features

    except Exception as e:
        print(f"Error computing ECG features with NeuroKit: {e}")
        return {}

def compute_gsr_features(gsr_signal_array):
    """
    Computes Skin Conductance Level (SCL) and Skin Conductance Responses (SCRs).
    Handles potential NeuroKit warnings/errors and NaN values.
    """
    # Pre-check for flat or invalid signal
    if not np.any(np.isfinite(gsr_signal_array)) or np.all(gsr_signal_array == gsr_signal_array[0]):
        return {}
    if len(gsr_signal_array) < SAMPLING_RATE * 5: # Recommended minimum 5 seconds for GSR analysis
        return {}

    features = {}
    try:
        eda_signals, info = nk.eda_process(gsr_signal_array, sampling_rate=SAMPLING_RATE)

        # 1. Skin Conductance Level (SCL) - Tonic component
        if "EDA_Tonic" in eda_signals.columns and not eda_signals["EDA_Tonic"].isnull().all():
            scl_val = eda_signals["EDA_Tonic"].mean()
            if not np.isnan(scl_val):
                features['gsr_scl'] = round(scl_val, 4)

        # 2. Skin Conductance Responses (SCRs) - Phasic component
        if "SCR_Amplitude" in info and len(info["SCR_Amplitude"]) > 0 and np.any(np.isfinite(info["SCR_Amplitude"])):
            scr_amplitudes = np.array(info["SCR_Amplitude"])
            features['gsr_num_scrs'] = len(scr_amplitudes)
            features['gsr_avg_scr_amp'] = round(np.nanmean(scr_amplitudes), 4)
        else:
            features['gsr_num_scrs'] = 0
            features['gsr_avg_scr_amp'] = 0.0

        return features

    except Exception as e:
        print(f"Error computing GSR features with NeuroKit: {e}")
        return {}

def compute_ppg_features(bvp_signal_array):
    """
    Computes Perfusion Index (PI) from BVP (PPG) signal.
    Handles potential errors and NaN values.
    """
    # Pre-check for flat or invalid signal
    if not np.any(np.isfinite(bvp_signal_array)) or np.all(bvp_signal_array == bvp_signal_array[0]):
        return {}
    if len(bvp_signal_array) < SAMPLING_RATE * 1: # Need at least 1 second for basic PI
        return {}

    features = {}
    try:
        # DC component: Mean of the signal
        dc_component = np.mean(bvp_signal_array)

        # AC component: Difference between the 95th and 5th percentile for robustness
        ac_component = np.percentile(bvp_signal_array, 95) - np.percentile(bvp_signal_array, 5)

        if dc_component != 0 and not np.isnan(ac_component) and not np.isnan(dc_component):
            features['ppg_perfusion_index'] = round((ac_component / dc_component) * 100, 2)
        else:
            features['ppg_perfusion_index'] = 0.0

        return features

    except Exception as e:
        print(f"Error computing PPG features: {e}")
        return {}

# --- Main Consumer Loop ---
print("Starting to consume messages from SensorData topic...")
try:
    for message in consumer:
        data: dict = message.value
        current_device_id = data.get('deviceId')

        if not current_device_id:
            print("Skipping message: 'deviceId' not found.")
            continue

        # Get buffers for the current device
        buffers = device_buffers[current_device_id]

        # Append data to respective buffers if present in the current message
        if data.get('ecg') is not None:
            buffers['ecg'].append(data['ecg'])
        if data.get('bvp') is not None:
            buffers['bvp'].append(data['bvp'])
        if data.get('gsr') is not None:
            buffers['gsr'].append(data['gsr'])
        if data.get('timestamp') is not None:
            buffers['timestamp'].append(data['timestamp'])

        # Initialize last_processed_time for new devices
        if current_device_id not in last_processed_time:
            last_processed_time[current_device_id] = time.time()

        current_time = time.time()

        # Process features if it's time to process for this device
        if (current_time - last_processed_time[current_device_id]) >= PROCESS_INTERVAL_SECONDS:

            # Initialize a dictionary for all features, common for all outputs
            all_features = {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'deviceId': current_device_id,
            }
            
            # Flags to check if any sensor data was actually processed and features computed
            ecg_processed = False
            bvp_processed = False
            gsr_processed = False

            # --- ECG Processing ---
            # Only process ECG if the buffer is full AND the current message contained ECG data
            if len(buffers['ecg']) == BUFFER_SIZE_SAMPLES and data.get('ecg') is not None:
                ecg_array = np.array(list(buffers['ecg']))
                ecg_features = compute_ecg_features(ecg_array)
                if ecg_features: # Only update if features were successfully computed (not empty)
                    all_features.update(ecg_features)
                    ecg_processed = True
                # Clear buffer if you want non-overlapping windows after processing
                # buffers['ecg'].clear() # Uncomment if you want discrete, non-overlapping windows

            # --- GSR Processing ---
            # Only process GSR if the buffer is full AND the current message contained GSR data
            if len(buffers['gsr']) == BUFFER_SIZE_SAMPLES and data.get('gsr') is not None:
                gsr_array = np.array(list(buffers['gsr']))
                gsr_features = compute_gsr_features(gsr_array)
                if gsr_features:
                    all_features.update(gsr_features)
                    gsr_processed = True
                # buffers['gsr'].clear() # Uncomment if you want discrete, non-overlapping windows

            # --- PPG (BVP) Processing ---
            # Only process BVP if the buffer is full AND the current message contained BVP data
            if len(buffers['bvp']) == BUFFER_SIZE_SAMPLES and data.get('bvp') is not None:
                bvp_array = np.array(list(buffers['bvp']))
                ppg_features = compute_ppg_features(bvp_array)
                if ppg_features:
                    all_features.update(ppg_features)
                    bvp_processed = True
                # buffers['bvp'].clear() # Uncomment if you want discrete, non-overlapping windows

            # Publish the consolidated features ONLY if at least one type of feature was processed
            # and the dictionary contains more than just 'timestamp' and 'deviceId'
            if producer and (ecg_processed or bvp_processed or gsr_processed) and len(all_features) > 2:
                producer.send("hrData", all_features)
                print(f"Published features for device {current_device_id}: {all_features}")
            else:
                # print(f"No sufficient or valid features to publish for device {current_device_id} at this interval.")
                pass # Silently skip if no features were computed

            # Update last processed time for this device regardless of whether features were published
            # This ensures processing attempts happen at regular intervals
            last_processed_time[current_device_id] = current_time

except KeyboardInterrupt:
    print("\nExiting consumer loop.")
finally:
    if producer:
        producer.close()
        print("Producer closed.")
    if consumer:
        consumer.close()
        print("Consumer closed.")