import paho.mqtt.client as mqtt
import argparse
import csv
import json
import threading
import datetime
import time
from math import floor

# Remove the global start_time
# start_time = datetime.datetime.utcnow()

def get_dict_from_data(row, file_number):
    data = {}
    try:
        # We don't need the offset_seconds to create a "future" timestamp
        # if the goal is to send data as it "happens"
        # However, if your CSV data represents offsets from some *actual* event time
        # then you should re-evaluate how these offsets relate to current time.
        # For typical sensor data, you'd want the timestamp to be the current time of measurement.

        # Let's assume for now the row[0] is just an index or relative time
        # and you want the actual timestamp to be when the message is sent.
        # If row[0] represents seconds from the start of the *file's* recording,
        # and you want to simulate that, you'd need a different approach.

        # Option 1: Timestamp is the current UTC time when the message is prepared
        dt = datetime.datetime.utcnow()
        data["timestamp"] = dt.isoformat() + "Z"

        # Option 2: If row[0] is a *duration* from the very beginning of the script's run,
        # and you want to simulate data coming in "real-time" from an event that started
        # when the script launched, then you'd need the initial start_time.
        # In that case, you might need to adjust the start_time at midnight or restart the script.
        # However, for continuous data streams, Option 1 is usually preferred.

    except Exception as e:
        print(f"Timestamp conversion error for row {row}: {e}")
        return None

    try:
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
            if data:
                mqttc.publish("sensors", json.dumps(data))
                print(f"Published: {data}")
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