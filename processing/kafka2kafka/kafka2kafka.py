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


ecg_buffer = collections.deque(maxlen=BUFFER_SIZE_SAMPLES)
bvp_buffer = collections.deque(maxlen=BUFFER_SIZE_SAMPLES)
gsr_buffer = collections.deque(maxlen=BUFFER_SIZE_SAMPLES)
timestamp_buffer = collections.deque(maxlen=BUFFER_SIZE_SAMPLES) # Not strictly needed for features, but good for context

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
        # print("Warning: ECG signal is flat or invalid. Skipping ECG feature computation.")
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
        # print("Warning: GSR signal is flat or invalid. Skipping GSR feature computation.")
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
        # Use np.nanmean to safely average, ignoring NaNs if present
        # Check if 'SCR_Amplitude' exists AND contains valid, non-NaN amplitudes
        if "SCR_Amplitude" in info and len(info["SCR_Amplitude"]) > 0 and np.any(np.isfinite(info["SCR_Amplitude"])):
            scr_amplitudes = np.array(info["SCR_Amplitude"])
            features['gsr_num_scrs'] = len(scr_amplitudes)
            features['gsr_avg_scr_amp'] = round(np.nanmean(scr_amplitudes), 4)
        else:
            features['gsr_num_scrs'] = 0
            features['gsr_avg_scr_amp'] = 0.0 # Set to 0 if no SCRs or valid amplitudes

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
        # print("Warning: BVP signal is flat or invalid. Skipping PPG feature computation.")
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
            features['ppg_perfusion_index'] = 0.0 # Set to 0 if invalid components

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

        # Initialize last_processed_time for new devices
        if current_device_id not in last_processed_time:
            last_processed_time[current_device_id] = time.time()

        # Append data to respective buffers
        # Ensure values are not None before appending
        if data.get('ecg') is not None:
            ecg_buffer.append(data['ecg'])
        if data.get('bvp') is not None:
            bvp_buffer.append(data['bvp'])
        if data.get('gsr') is not None:
            gsr_buffer.append(data['gsr'])
        if data.get('timestamp') is not None:
            timestamp_buffer.append(data['timestamp'])

        # Process features if buffer is full enough and it's time to process
        current_time = time.time()
        # Ensure buffers are sufficiently filled BEFORE attempting to process
        if (len(ecg_buffer) == BUFFER_SIZE_SAMPLES and
            len(bvp_buffer) == BUFFER_SIZE_SAMPLES and
            len(gsr_buffer) == BUFFER_SIZE_SAMPLES and
            (current_time - last_processed_time[current_device_id]) >= PROCESS_INTERVAL_SECONDS):

            # Convert deques to numpy arrays for NeuroKit2
            # Use np.array(list(deque)) to ensure it's a regular NumPy array
            ecg_array = np.array(list(ecg_buffer))
            bvp_array = np.array(list(bvp_buffer))
            gsr_array = np.array(list(gsr_buffer))

            # Initialize a dictionary for all features
            all_features = {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'deviceId': current_device_id,
            }

            # Compute and add ECG features
            ecg_features = compute_ecg_features(ecg_array)
            all_features.update(ecg_features)

            # Compute and add GSR features
            gsr_features = compute_gsr_features(gsr_array)
            all_features.update(gsr_features)

            # Compute and add PPG features
            ppg_features = compute_ppg_features(bvp_array)
            all_features.update(ppg_features)

            # Publish the consolidated features
            if producer:
                # Use 'PhysiologicalFeatures' topic for processed data
                producer.send("hrData", all_features)
                print(f"Published features for device {current_device_id}: {all_features}")

            # Update last processed time for this device
            last_processed_time[current_device_id] = current_time

            # Note: Deques automatically handle trimming to maxlen.
            # No explicit pop(0) or clear needed if you want overlapping windows.

except KeyboardInterrupt:
    print("\nExiting consumer loop.")
finally:
    if producer:
        producer.close()
        print("Producer closed.")
    if consumer:
        consumer.close()
        print("Consumer closed.")