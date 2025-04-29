import paho.mqtt.client as mqtt
import argparse
import csv
import json
import threading
import time

def get_json_data(row, file_number):
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

    data["file_number"] = file_number
    return json.dumps(data)

def process_file(file, file_number, mqttc):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            json_data = get_json_data(row, file_number)
            if json_data:
                mqttc.publish("sensors", json_data)
                print(f"Sensor data is sent: {json_data}")
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

if __name__ == "__main__":
    main()
