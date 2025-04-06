import time
import json
import random
import csv

from kafka import KafkaProducer

def get_json_data(row):
    data = {}
    try:
        dt = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        data["timestamp"] = dt.isoformat() + "Z" 
    except Exception as e:
        data["timestamp"] = row[0]  

        data["bvp"] = float(row[1])
        data["gsr"] = float(row[2])
    except ValueError:
        return None

    return json.dumps(data)
def main():
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    with open("sub_1.csv", 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            json_data = get_json_data(row)
            producer.send('SensorData', bytes(f'{json_data}','UTF-8'))
            print(f"Sensor data is sent: {json_data}")
            time.sleep(0.2)


if __name__ == "__main__":
    main()