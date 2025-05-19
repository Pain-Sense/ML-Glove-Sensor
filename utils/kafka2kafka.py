from kafka import KafkaProducer, KafkaConsumer
import json

KAFKA_ADDRESS = 'localhost:9094'

producer = KafkaProducer(bootstrap_servers=[KAFKA_ADDRESS])
consumer = KafkaConsumer(
    'SensorData',
    bootstrap_servers=[KAFKA_ADDRESS],
    auto_offset_reset='earliest',  # Start consuming from the earliest message if no offset is committed
    enable_auto_commit=True,  # Automatically commit offsets
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# print(f"bootstrap_connected: {consumer.bootstrap_connected()}")

while True:
    for message in consumer:
        data: dict = message.value
        producer.send("hrData", json.dumps(data).encode('utf-8'))
