Comandos para dar boot. (to be changed)
./mvnw quarkus:dev

docker compose up

telegraf --config telegraf.conf 

python3 garden_sensor_gateway.py 


docker exec -it kafka bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic garden_sensor_data  --from-beginning

curl -X POST http://localhost:8089/kafka/send
