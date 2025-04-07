import os
import time
import json
import csv
import datetime
from kafka import KafkaProducer
import threading

def get_json_data(row, file_number):
    data = {}
    try:
        dt = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        data["timestamp"] = dt.isoformat() + "Z"
    except Exception:
        data["timestamp"] = row[0]

    try:
        data["bvp"] = float(row[2])
        data["gsr"] = float(row[3])
    except ValueError:
        return None

    data["file_number"] = file_number
    return json.dumps(data)

def process_file(file, file_number, producer):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            json_data = get_json_data(row, file_number)
            if json_data:
                producer.send('SensorData', json_data.encode('utf-8'))
                # print(f"Sensor data is sent: {json_data}")
                time.sleep(0.1)

def create_producer():
    kafka_broker = os.getenv('KAFKA_BROKER', 'kafka:9092')
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers=[kafka_broker])
            return producer
        except Exception as e:
            print(f"Error connecting to Kafka: {e}, retrying in 5 seconds...")
            time.sleep(5)

def main():
    data_dir = os.getenv("DATA_DIR", "./data")

    producer = create_producer()
    threads = []

    for file_number in range(1, 6):
        file_path = os.path.join(data_dir, f"sub_{file_number}.csv")
        thread = threading.Thread(target=process_file, args=(file_path, file_number, producer))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
