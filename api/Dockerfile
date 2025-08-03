FROM python:3.9-slim

WORKDIR /app  # Must match compose volume mount
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]  # Adjust as needed