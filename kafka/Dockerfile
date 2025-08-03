# Use official Python image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt if you have one
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python scripts into the container
COPY producer.py .
COPY consumer.py .

# Default command: run producer (you can override in docker-compose or CLI)
CMD ["python", "producer.py"]
