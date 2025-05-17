import paho.mqtt.client as mqtt
import argparse
import json
import threading
import datetime
import time
import random

MQTT_TOPIC = "sensors"
PUBLISH_INTERVAL = 1  # Time in seconds between messages
BATCH_SIZE = 10

buffer = []
lock = threading.Lock()

def generate_random_data(device_id):
    data = {}
    dt = datetime.datetime.utcnow()
    data["timestamp"] = dt.isoformat() + "Z"
    data["bvp"] = round(random.uniform(30.0, 40.0), 3)
    data["gsr"] = round(random.uniform(10.0, 15.0), 3)
    data["deviceId"] = device_id
    return data

def batch_publisher(mqttc):
    while True:
        time.sleep(PUBLISH_INTERVAL)
        with lock:
            if buffer:
                payload = {
                    "deviceId": buffer[0]["deviceId"],
                    "readings": buffer[:]
                }
                mqttc.publish(MQTT_TOPIC, json.dumps(payload))
                print(f"Published batch: {payload}")
                buffer.clear()

def simulate_data(device_id, mqttc):
    print(f"Starting to send random data for Device {device_id}.")
    while True:
        data = generate_random_data(device_id)
        with lock:
            buffer.append(data)
            if len(buffer) >= BATCH_SIZE:
                payload = {
                    "deviceId": device_id,
                    "readings": buffer[:]
                }
                mqttc.publish(MQTT_TOPIC, json.dumps(payload))
                print(f"Published batch: {payload}")
                buffer.clear()
        time.sleep(PUBLISH_INTERVAL)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--addr', type=str, default="localhost", help="Endereço do broker MQTT.")
    parser.add_argument('-p', '--port', type=int, default=1883, help="Porto do broker MQTT.")
    args = parser.parse_args()

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    connected = False
    while not connected:
        try:
            mqttc.connect(args.addr, args.port)
            connected = True
            print("Connected to MQTT broker")
        except Exception as e:
            print(f"Connection failed, retrying in 5 seconds... {e}")
            time.sleep(5)

    mqttc.loop_start()

    threading.Thread(target=batch_publisher, args=(mqttc,), daemon=True).start()

    threads = []
    for device_id in range(1, 4):  # Start three devices
        thread = threading.Thread(target=simulate_data, args=(device_id, mqttc))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Simulation finished.")

if __name__ == "__main__":
    main()
