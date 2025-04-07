FROM python:3.8-slim

# Set working directory inside container
WORKDIR /app

# Copy the current directory (containing your code) into the container's /app directory
COPY . /app

# Install dependencies if any (for example, from requirements.txt)
RUN pip install -r requirements.txt

# Set the command to run the script
CMD ["python", "main.py"]
