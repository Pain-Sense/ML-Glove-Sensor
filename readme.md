## 📦 Requirements

- Docker & Docker Compose  
- Java 17+ (for Quarkus)  
- Python 3.8+ (optional if running the producer manually)  
- Maven wrapper (`./mvnw`)

---

## 🚀 Getting Started

All major components are orchestrated using `docker-compose`. Use `make` to manage the workflow easily.

### 🛠 Run the Full Stack

```bash
make up                # Start the full stack (Kafka, Spark, Influx, etc.)
make quarkus           # Run Quarkus in development mode
make consume-raw       # Listen to raw sensor data on Kafka topic 'SensorData'
make consume-processed # Listen to processed data on topic 'ProcessedSensorData'
make post              # Send test POST request to Quarkus endpoint
make logs              # Tail logs from all running services
make down             # Stop all containers and remove associated volumes
