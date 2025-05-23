import paho.mqtt.client as mqtt
import argparse
import csv
import json
import threading
import datetime
import time
from math import floor

# Global start time for all devices/files
#change teste para eniar mensagens com um timestamp especifico 
start_time = datetime.datetime.utcnow() - datetime.timedelta(hours=1)

def get_dict_from_data(row, file_number):
    data = {}
    try:
        offset_seconds = float(row[0])
        dt = start_time + datetime.timedelta(seconds=offset_seconds)
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

def process_file(file, file_number, mqttc, topic_name):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        print(f"Starting to send data from {file}.")

        for row in reader:
            data = get_dict_from_data(row, file_number)
            if data:
                mqttc.publish(topic_name, json.dumps(data))
                print(f"Published: {data}")
                time.sleep(0.005)

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
    parser.add_argument(
    '-t', '--topic', type=str, default="sensors",
    help="Tópico de destino."
)

    args = parser.parse_args()

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.connect(args.addr, args.port)
    mqttc.loop_start()

    threads = []

    for file_number in range(1, 3):
        file = f"Data/sub_{file_number}.csv"
        thread = threading.Thread(target=process_file, args=(file, file_number, mqttc, args.topic))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All data has been sent.")

if __name__ == "__main__":
    main()
    