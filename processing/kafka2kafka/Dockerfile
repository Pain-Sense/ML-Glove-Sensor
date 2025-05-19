# Use a lightweight Python image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first and install them
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY kafka2kafka.py .

# A script to make us wait until Kafka is ready.
COPY wait-for-it.sh .
RUN chmod +x ./wait-for-it.sh

# Default command to run your producer script
ENTRYPOINT ["./wait-for-it.sh", "-t", "60", "-s", "kafka:9092", "--", "python", "kafka2kafka.py", "-a", "kafka:9092"]
