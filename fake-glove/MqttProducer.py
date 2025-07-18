import paho.mqtt.client as mqtt
import argparse
import csv
import json
import threading
import datetime
import time
from math import floor
def get_dict_from_data(row, file_number):
    data = {}
    try:

        dt = datetime.datetime.utcnow()
        data["timestamp"] = dt.isoformat() + "Z"

    except Exception as e:
        print(f"Timestamp conversion error for row {row}: {e}")
        return None

    try:
        data["ecg"] = float(row[1])
        data["bvp"] = float(row[2])
        data["gsr"] = float(row[3])
    except ValueError as e:
        print(f"Value conversion error for row {row}: {e}")
        return None

    data["deviceId"] = file_number
    return data

def process_file(file, file_number, mqttc):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        print(f"Starting to send data from {file}.")

        for row in reader:
            data = get_dict_from_data(row, file_number)
            if not data:
                continue

                # Device 2
            if file_number == 2:
                gsr_message = {
                    "deviceId": data["deviceId"],
                    "timestamp": data["timestamp"],
                    "value": data["gsr"]
                }

                sensors_message = {
                    "deviceId": data["deviceId"],
                    "timestamp": data["timestamp"],
                    "gsr": data["gsr"]
                }
                mqttc.publish("sensors", json.dumps(sensors_message))
                print(f"Published to sensors: {sensors_message}")
                mqttc.publish("sensors/gsr", json.dumps(gsr_message))
                print(f"Published to sensors/gsr: {gsr_message}")
            else:
                # Device 1 
                mqttc.publish("sensors", json.dumps(data))
                print(f"Published to sensors: {data}")

                for field in ["ecg", "bvp", "gsr"]:
                    message = {
                        "deviceId": data["deviceId"],
                        "timestamp": data["timestamp"],
                        "value": data[field]
                    }
                    topic = f"sensors/{field}"
                    mqttc.publish(topic, json.dumps(message))
                    print(f"Published to {topic}: {message}")

            time.sleep(0.01)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', '--addr', type=str, default="localhost",
        help="Endereço do broker MQTT."
    )
    parser.add_argument(
        '-p', '--port', type=int, default=1883,
        help="Porto do broker MQTT."
    )

    args = parser.parse_args()

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.connect(args.addr, args.port)
    mqttc.loop_start()

    threads = []

    for file_number in range(1, 3):
        file = f"Data/sub_{file_number}.csv"
        thread = threading.Thread(target=process_file, args=(file, file_number, mqttc))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All data has been sent.")

if __name__ == "__main__":
    main()