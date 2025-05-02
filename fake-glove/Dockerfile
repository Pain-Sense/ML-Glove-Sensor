# Use a lightweight Python image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first and install them
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY *.py .

# Copy the dataset.
COPY ./Data Data

# Default command to run your producer script
ENTRYPOINT ["python", "MqttProducer.py"]
CMD ["-a", "mosquitto"]
