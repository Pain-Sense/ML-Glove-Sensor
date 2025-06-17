# mqtt_multi_device_publisher.py
import paho.mqtt.client as mqtt
import time
import json
import csv
from datetime import datetime, timezone
from threading import Thread

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors"
NUM_MESSAGES = 10000  # per device
FREQ_HZ = 50
DELAY = 1 / FREQ_HZ
NUM_DEVICES = 20
DEVICE_ID_START = 45
DEVICE_ID_END = 65  # inclusive
def publish_device_data(device_id):
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER, PORT)
    client.loop_start()

    log = []
    for seq in range(NUM_MESSAGES):
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        message = {
            "timestamp": now,
            "ecg": 0.784,
            "bvp": 35.857,
            "gsr": 5.122,
            "deviceId": device_id,
            "seq": seq
        }
        payload = json.dumps(message)
        client.publish(TOPIC, payload)
        log.append((seq, now))
        if seq % 1000 == 0:
            print(f"📡 Device {device_id}: Sent {seq} messages")
        time.sleep(DELAY)

    client.loop_stop()
    client.disconnect()

    filename = f"sent_messages_device_{device_id}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["seq", "sent_timestamp"])
        writer.writerows(log)
    print(f"✅ Device {device_id} done sending {NUM_MESSAGES} messages.")

# Launch threads for 20 devices
threads = []
for device_id in range(DEVICE_ID_START, DEVICE_ID_END + 1):
    thread = Thread(target=publish_device_data, args=(device_id,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("🚀 All devices finished publishing.")
