import json
import argparse
from collections import deque
import numpy as np
import neurokit2 as nk
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

DOWNSAMPLE_WINDOW = 10
BUFFER_SIZE = 200  # Increased buffer size
ECG_FS = 100  # Ensure this matches your sensor's sampling rate
BVP_FS = 50
GSR_FS = 10
MQTT_TOPIC = "sensors"

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
    '--influxdb-url',
    type=str, default="http://localhost:8086",
    help="URL of the InfluxDB instance."
)
parser.add_argument(
    '--influxdb-token',
    type=str, required=True,
    help="Token for authenticating with InfluxDB."
)
parser.add_argument(
    '--influxdb-org',
    type=str, required=True,
    help="Organization in InfluxDB."
)
parser.add_argument(
    '--influxdb-bucket',
    type=str, required=True,
    help="Bucket in InfluxDB."
)

args = parser.parse_args()

ecg_buffer = deque(maxlen=BUFFER_SIZE)
bvp_buffer = deque(maxlen=BUFFER_SIZE)
gsr_buffer = deque(maxlen=BUFFER_SIZE)

ecg_downsampled_buffer = deque()
bvp_downsampled_buffer = deque()
gsr_downsampled_buffer = deque()

# Initialize InfluxDB client
influxdb_client = InfluxDBClient(url=args.influxdb_url, token=args.influxdb_token, org=args.influxdb_org)
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker at {args.broker}:{args.port}")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"Failed to connect to MQTT Broker, return code {rc}")

def on_message(client, userdata, msg):
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

            if len(ecg_buffer) == BUFFER_SIZE:
                print("Processing ECG with neurokit2...")
                ecg_signal = np.array(list(ecg_buffer))
                try:
                    ecg_processed = nk.ecg_process(ecg_signal, sampling_rate=ECG_FS)
                    heart_rate = np.mean(ecg_processed["ECG_Rate"])
                    ecg_downsampled_buffer.append(heart_rate)
                    print(f"ECG processed, heart rate: {heart_rate}")
                except Exception as e:
                    print(f"Error processing ECG: {e}")

            if len(bvp_buffer) == BUFFER_SIZE:
                print("Processing BVP with neurokit2...")
                bvp_signal = np.array(list(bvp_buffer))
                try:
                    bvp_processed = nk.ppg_process(bvp_signal, sampling_rate=BVP_FS)
                    bvp_downsampled_buffer.append(np.mean(bvp_processed["PPG_Rate"]))
                    print("BVP processed")
                except Exception as e:
                    print(f"Error processing BVP: {e}")

            if len(gsr_buffer) == BUFFER_SIZE:
                print("Processing GSR with neurokit2...")
                gsr_signal = np.array(list(gsr_buffer))
                try:
                    gsr_processed = nk.eda_process(gsr_signal, sampling_rate=GSR_FS)
                    gsr_downsampled_buffer.append(np.mean(gsr_processed["EDA_Phasic"]))
                    print("GSR processed")
                except Exception as e:
                    print(f"Error processing GSR: {e}")

            processed_data = {
                'timestamp': timestamp,
                'heart_rate': list(ecg_downsampled_buffer)[-1] if ecg_downsampled_buffer else None,
                'downsampled_ecg': list(ecg_downsampled_buffer)[-1] if ecg_downsampled_buffer else None,
                'downsampled_bvp': list(bvp_downsampled_buffer)[-1] if bvp_downsampled_buffer else None,
                'downsampled_gsr': list(gsr_downsampled_buffer)[-1] if gsr_downsampled_buffer else None,
                'deviceId': device_id
            }
            print(f"Sending processed data to InfluxDB: {processed_data}")

            # Write data to InfluxDB
            point = Point("sensor_data") \
                .tag("deviceId", str(device_id)) \
                .field("heart_rate", processed_data['heart_rate']) \
                .field("downsampled_ecg", processed_data['downsampled_ecg']) \
                .field("downsampled_bvp", processed_data['downsampled_bvp']) \
                .field("downsampled_gsr", processed_data['downsampled_gsr']) \
                .time(timestamp, WritePrecision.NS)

            write_api.write(args.influxdb_bucket, args.influxdb_org, point)
            print("Processed data sent to InfluxDB.")

            # Clear buffers after processing
            ecg_buffer.clear()
            bvp_buffer.clear()
            gsr_buffer.clear()

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(args.broker, args.port, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("Received keyboard interrupt; exiting.")
finally:
    client.disconnect()
    print("MQTT client disconnected.")
    influxdb_client.close()
    print("InfluxDB client closed.")
