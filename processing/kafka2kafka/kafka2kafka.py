from kafka import KafkaProducer, KafkaConsumer
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    '-a', '--address', '--bootstrap-address',
    type=str, default="localhost:9094",
    help="Endereço do broker Kafka."
)

args = parser.parse_args();

try:
    producer = KafkaProducer(bootstrap_servers=[args.address])
    consumer = KafkaConsumer(
        'SensorData',
        bootstrap_servers=[args.address],
        auto_offset_reset='earliest',  # Start consuming from the earliest message if no offset is committed
        enable_auto_commit=True,  # Automatically commit offsets
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    # print(f"bootstrap_connected: {consumer.bootstrap_connected()}")

    while True:
        for message in consumer:
            data: dict = message.value
            producer.send("hrData", json.dumps(data).encode('utf-8'))
except KeyboardInterrupt:
    print("Received keyboard interrupt; exiting.")
