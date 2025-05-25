import json
import argparse
from collections import deque
import numpy as np
from scipy.signal import butter, lfilter, sosfilt
import paho.mqtt.client as mqtt
from kafka import KafkaProducer

DOWNSAMPLE_WINDOW = 10
BUFFER_SIZE = 1000  # Adjust based on your expected sampling rate and filter requirements
ECG_FS = 100  # Example sampling rate for ECG (Hz) - Adjust based on your sensor
BVP_FS = 50    # Example sampling rate for BVP (Hz) - Adjust based on your sensor
GSR_FS = 10    # Example sampling rate for GSR (Hz) - Adjust based on your sensor
MQTT_TOPIC = "sensors"
KAFKA_TOPIC = "filtered_sensors"  # Topic to send processed data to

# --- Filter Design ---

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], btype='band', analog=False, output='sos')
    
    y = sosfilt(sos, data)
    return y
def butter_lowpass_filter(data, cutoff, fs, order=5):   
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    sos = butter(order, normal_cutoff, btype='low', analog=False, output='sos')

    y = sosfilt(sos, data)
    return y

parser = argparse.ArgumentParser()
parser.add_argument(
    '-b', '--broker',
    type=str, default="localhost",
    help="Address of the MQTT broker."
)
parser.add_argument(
    '-p', '--port',
    type=int, default=1883,
    help="Port of the MQTT broker."
)
parser.add_argument(
    '-k', '--kafka-address', '--bootstrap-address',
    type=str, default="localhost:9092",
    help="Address of the Kafka broker."
)

args = parser.parse_args();

ecg_buffer = deque(maxlen=BUFFER_SIZE)
bvp_buffer = deque(maxlen=BUFFER_SIZE)
gsr_buffer = deque(maxlen=BUFFER_SIZE)

ecg_filtered_buffer = deque()
bvp_filtered_buffer = deque()
gsr_filtered_buffer = deque()

ecg_downsampled_buffer = deque()
bvp_downsampled_buffer = deque()
gsr_downsampled_buffer = deque()

ecg_counter = 0
bvp_counter = 0
gsr_counter = 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker at {args.broker}:{args.port}")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"Failed to connect to MQTT Broker, return code {rc}")

def on_message(client, userdata, msg):
    global ecg_counter, bvp_counter, gsr_counter, kafka_producer
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
    try:
        data: dict = json.loads(msg.payload.decode())
        timestamp = data.get('timestamp')
        ecg_value = data.get('ecg')
        bvp_value = data.get('bvp')
        gsr_value = data.get('gsr')
        device_id = data.get('deviceId')

        if all(v is not None for v in [ecg_value, bvp_value, gsr_value]):
            ecg_buffer.append(ecg_value)
            bvp_buffer.append(bvp_value)
            gsr_buffer.append(gsr_value)
            print(f"Appended values - ECG buffer size: {len(ecg_buffer)}, BVP buffer size: {len(bvp_buffer)}, GSR buffer size: {len(gsr_buffer)}")

            # --- Filtering ---
            if len(ecg_buffer) == BUFFER_SIZE:
                print("Filtering ECG...")
                ecg_filtered = butter_bandpass_filter(np.array(list(ecg_buffer)), 0.5, 40, ECG_FS, order=3)
                ecg_filtered_buffer.extend(ecg_filtered.tolist())
                ecg_buffer.clear() # Clear the buffer after processing
                print(f"ECG filtered, filtered buffer size: {len(ecg_filtered_buffer)}")

            if len(bvp_buffer) == BUFFER_SIZE:
                print("Filtering BVP...")
                bvp_filtered = butter_bandpass_filter(np.array(list(bvp_buffer)), 0.5, 4, BVP_FS, order=3)
                bvp_filtered_buffer.extend(bvp_filtered.tolist())
                bvp_buffer.clear() # Clear the buffer after processing
                print(f"BVP filtered, filtered buffer size: {len(bvp_filtered_buffer)}")

            if len(gsr_buffer) == BUFFER_SIZE:
                print("Filtering GSR...")
                gsr_filtered = butter_lowpass_filter(np.array(list(gsr_buffer)), 1.0, GSR_FS, order=3)
                gsr_filtered_buffer.extend(gsr_filtered.tolist())
                gsr_buffer.clear() # Clear the buffer after processing
                print(f"GSR filtered, filtered buffer size: {len(gsr_filtered_buffer)}")

            # --- Downsampling ---
            if ecg_filtered_buffer:
                print("Downsampling ECG...")
                ecg_counter += len(ecg_filtered_buffer)
                if ecg_counter // DOWNSAMPLE_WINDOW > 0 and (ecg_counter // DOWNSAMPLE_WINDOW) <= len(ecg_filtered_buffer):
                    downsampled_value = ecg_filtered_buffer[(ecg_counter // DOWNSAMPLE_WINDOW) - 1]
                    ecg_downsampled_buffer.append(downsampled_value)
                    print(f"ECG downsampled, value: {downsampled_value}, downsampled buffer size: {len(ecg_downsampled_buffer)}")
                ecg_filtered_buffer.clear()
                ecg_counter = 0 # Reset counter after downsampling
            if bvp_filtered_buffer:
                print("Downsampling BVP...")
                bvp_counter += len(bvp_filtered_buffer)
                if bvp_counter // DOWNSAMPLE_WINDOW > 0 and (bvp_counter // DOWNSAMPLE_WINDOW) <= len(bvp_filtered_buffer):
                    downsampled_value = bvp_filtered_buffer[(bvp_counter // DOWNSAMPLE_WINDOW) - 1]
                    bvp_downsampled_buffer.append(downsampled_value)
                    print(f"BVP downsampled, value: {downsampled_value}, downsampled buffer size: {len(bvp_downsampled_buffer)}")
                bvp_filtered_buffer.clear()
                bvp_counter = 0 # Reset counter after downsampling

            if gsr_filtered_buffer:
                print("Downsampling GSR...")
                gsr_counter += len(gsr_filtered_buffer)
                if gsr_counter // DOWNSAMPLE_WINDOW > 0 and (gsr_counter // DOWNSAMPLE_WINDOW) <= len(gsr_filtered_buffer):
                    downsampled_value = gsr_filtered_buffer[(gsr_counter // DOWNSAMPLE_WINDOW) - 1]
                    gsr_downsampled_buffer.append(downsampled_value)
                    print(f"GSR downsampled, value: {downsampled_value}, downsampled buffer size: {len(gsr_downsampled_buffer)}")
                gsr_filtered_buffer.clear()
                gsr_counter = 0 # Reset counter after downsampling

            # --- Heart Rate Extraction (Illustrative - Needs Proper Implementation) ---
            heart_rate = None
            if ecg_downsampled_buffer and len(ecg_downsampled_buffer) > 1:
                diff = np.diff(list(ecg_downsampled_buffer))
                peak_indices = np.where(diff > 0.2)[0] # Adjust threshold
                if len(peak_indices) > 1:
                    time_diff = (len(ecg_downsampled_buffer) / (ECG_FS / DOWNSAMPLE_WINDOW)) / (len(peak_indices) - 1) if (len(peak_indices) - 1) > 0 else None
                    if time_diff:
                        heart_rate = 60 / time_diff
                        print(f"Estimated Heart Rate: {heart_rate}")

            processed_data = {
                'timestamp': timestamp,
                'heart_rate': heart_rate,
                'downsampled_ecg': list(ecg_downsampled_buffer)[-1] if ecg_downsampled_buffer else None,
                'downsampled_bvp': list(bvp_downsampled_buffer)[-1] if bvp_downsampled_buffer else None,
                'downsampled_gsr': list(gsr_downsampled_buffer)[-1] if gsr_downsampled_buffer else None,
                'deviceId': device_id
            }
            print(f"Sending processed data to Kafka topic '{KAFKA_TOPIC}': {processed_data}")
            producer.send("filter", json.dumps(processed_data).encode('utf-8'))
            
            print("Processed data sent to Kafka topic.")

            # Clear downsampled buffers periodically to prevent memory buildup if needed
            if len(ecg_downsampled_buffer) > 100: # Adjust as needed
                ecg_downsampled_buffer.popleft()
                print("Removed oldest ECG downsampled value.")
            if len(bvp_downsampled_buffer) > 100:
                bvp_downsampled_buffer.popleft()
                print("Removed oldest BVP downsampled value.")
            if len(gsr_downsampled_buffer) > 100:
                gsr_downsampled_buffer.popleft()
                print("Removed oldest GSR downsampled value.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    producer = KafkaProducer(bootstrap_servers=["localhost:9094"])
    print(f"Connected to Kafka broker at: {"localhost:9094"}")
    client.connect(args.broker, args.port, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("Received keyboard interrupt; exiting.")
finally:
    client.disconnect()
    print("MQTT client disconnected.")
    if 'kafka_producer' in locals():
        producer.close()
        print("Kafka producer closed.")