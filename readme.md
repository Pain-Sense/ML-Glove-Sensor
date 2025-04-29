Comandos para dar boot. (to be changed)

go to the code-with quarkus directory and run:

./mvnw package

then go back to the root and run:

# This will run all the services as docker containers
docker compose up --build

# Open a shell inside the container to be able to run the producer script
docker exec -it ml-glove-sensor-python-kafka-producer-1 bash

# Inside the container, run the producer manually:
python producer.py

# Grafana is available on: (username: admin and password: admin)
http://localhost:3000/

# for testing purposes you can call this endpoint to let quarkus service process some data from kafka
curl -X POST http://localhost:8089/kafka/send
