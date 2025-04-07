# Config
KAFKA_BROKER=kafka:9092
RAW_TOPIC=SensorData
PROCESSED_TOPIC=ProcessedSensorData

.PHONY: up down logs \
        quarkus build \
        consume-raw consume-processed post \
        ps

## 🔧 Start all services (including Kafka, Spark, InfluxDB, MySQL, etc.)
up:
	docker compose up -d

## 🧯 Stop all services
down:
	docker compose down --volumes

## 🛠 Build Docker images
build:
	docker compose build

## 🔍 See status of running containers
ps:
	docker compose ps

## 🪵 Tail logs from all containers
logs:
	docker compose logs -f

## 🚀 Start Quarkus in dev mode
quarkus:
	./code-with-quarkus/mvnw quarkus:dev

## 📡 Consume raw data from Kafka
consume-raw:
	docker exec -it kafka \
		bin/kafka-console-consumer.sh \
		--bootstrap-server $(KAFKA_BROKER) \
		--topic $(RAW_TOPIC) \
		--from-beginning

## 🔄 Consume processed data from Kafka
consume-processed:
	docker exec -it kafka \
		bin/kafka-console-consumer.sh \
		--bootstrap-server $(KAFKA_BROKER) \
		--topic $(PROCESSED_TOPIC) \
		--from-beginning

## 🧪 Send test POST request to Quarkus endpoint
post:
	curl -X POST http://localhost:8089/kafka/send
