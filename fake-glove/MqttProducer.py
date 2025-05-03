import paho.mqtt.client as mqtt
import argparse
import csv
import json
import threading
import time
from math import floor

def get_dict_from_data(row, file_number):
    data = {}
    try:
        dt = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        data["timestamp"] = dt.isoformat() + "Z"
    except Exception as e:
        data["timestamp"] = row[0]

    try:
        data["bvp"] = float(row[2])
        data["gsr"] = float(row[3])
    except ValueError:
        return None

    data["id"] = file_number
    return data

def process_file(file, file_number, mqttc):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        print("Starting to send data.")

        for row in reader:
            data = get_dict_from_data(row, file_number)
            if data:
                mqttc.publish("sensors", json.dumps(data))
                ts = floor(float(data["timestamp"]))
                if (ts > 0) and (ts % 1000 == 0):
                    print(f"Sent 1000 rows of sensor data. The latest was: {data}")
                time.sleep(0.1)

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

    for file_number in range(1, 6):
        file = f"Data/sub_{file_number}.csv"
        thread = threading.Thread(target=process_file, args=(file, file_number, mqttc))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All data has been sent.")

if __name__ == "__main__":
    main()
