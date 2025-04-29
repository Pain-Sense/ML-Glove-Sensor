Comandos para dar boot. (to be changed)

docker compose up

telegraf --config telegraf.conf 

./mvnw quarkus:dev

```bash
cd fake-glove
python -m venv venv
pip install -r requirements.txt
python MqttProducer.py
```

#Grafana:
#http://localhost:3000/

#username:admin
#password:admin

#raw data
docker exec -it kafka bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic SensorData  --from-beginning

#processed data
docker exec -it kafka bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic ProcessedSensorData  --from-beginning

#for testing purposes
curl -X POST http://localhost:8089/kafka/send
