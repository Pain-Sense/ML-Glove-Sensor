from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import time
import random

while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        break
    except NoBrokersAvailable:
        print("Kafka not available yet. Retrying in 2s...")
        time.sleep(2)

def generate_fake_sensor_data():
    return {
        "timestamp": time.time(),
        "sensor_id": "sensor-1",
        "GSR": round(random.uniform(0.2, 0.8), 3),
        "BVP": round(random.uniform(60, 100), 2)
    }

if __name__ == "__main__":
    while True:
        data = generate_fake_sensor_data()
        producer.send("SensorData", data)
        print(f"Sent: {data}")
        time.sleep(1)
