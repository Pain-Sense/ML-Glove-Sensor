Comandos para dar boot. (to be changed)

go to the code-with quarkus directory and run ./mvnw package

then

docker compose up --build

# Open a shell inside the container to be able to run the producer script
docker exec -it ml-glove-sensor-python-kafka-producer-1 bash

# Inside the container, run the producer manually:
python producer.py

#Grafana:
#http://localhost:3000/

#username:admin
#password:admin

#for testing purposes
curl -X POST http://localhost:8089/kafka/send
