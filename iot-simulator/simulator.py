import os
import glob
import pandas as pd
import time
import json
from kafka import KafkaProducer

# Kafka setup
producer = KafkaProducer(
    bootstrap_servers=os.getenv('KAFKA_BROKER', 'kafka:9092'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_csv_data(file_path):
    print(f"Sending data from {file_path}")
    df = pd.read_csv(file_path)

    for index, row in df.iterrows():
        data = row.to_dict()
        # Add file_number from filename (sub_1.csv -> 1)
        data["file_number"] = os.path.basename(file_path).split("_")[1].split(".")[0]
        producer.send('SensorData', data)
        print(f"Sent: {data}")
        time.sleep(0.5)  # 0.5s delay to simulate real device timing

if __name__ == "__main__":
    data_folder = '/app/data'  # Path inside container
    csv_files = glob.glob(os.path.join(data_folder, "sub_*.csv"))

    if not csv_files:
        print("No CSV files found in /data")
    else:
        for file_path in csv_files:
            send_csv_data(file_path)

    print("Finished sending all data.")
