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
    except Exception as e:
        data["timestamp"] = row[0]

    try:
        data["bvp"] = float(row[2])
        data["gsr"] = float(row[3])
    except ValueError:
        return None

    data["id"] = file_number
    return json.dumps(data)

def process_file(file, file_number, producer):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            json_data = get_json_data(row, file_number)
            if json_data:
                producer.send('SensorData', bytes(f'{json_data}', 'UTF-8'))
                print(f"Sensor data is sent: {json_data}")
                time.sleep(0.1)

def main():
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    threads = []

    for file_number in range(1, 6):  
        file = f"Data/sub_{file_number}.csv"
        thread = threading.Thread(target=process_file, args=(file, file_number, producer))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
