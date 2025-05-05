Comandos para dar boot. (to be changed)

# This will run all the services as docker containers
docker compose up --build

# Grafana is available on: (username: admin and password: admin)
http://localhost:3000/

# Frontend is available on
http://localhost:5173/


# Testing info

## Debug endpoints

### Get active devices

Returns a list of devices that are actively sending sensor data (recently seen on the `SensorData` Kafka topic).

```bash
curl http://localhost:8089/debug/devices/active
´´´