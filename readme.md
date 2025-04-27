Comandos para dar boot. (to be changed)

go to the code-with quarkus directory and run ./mvnw package

then

docker compose up --build

python3 SensorDataProducer.py 

#Grafana:
#http://localhost:3000/

#username:admin
#password:admin

#for testing purposes
curl -X POST http://localhost:8089/kafka/send
