Comandos para dar boot. (to be changed)
./mvnw quarkus:dev

docker compose up

telegraf --config telegraf.conf 

python3 SensorDataProducer.py 

#raw data
docker exec -it kafka bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic SensorData  --from-beginning

#processed data
docker exec -it kafka bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic ProcessedSensorData  --from-beginning

#for testing purposes
curl -X POST http://localhost:8089/kafka/send
