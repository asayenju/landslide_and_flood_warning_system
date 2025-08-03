from kafka import KafkaProducer
import json
import time

# Create a KafkaProducer instance
# bootstrap_servers specifies the Kafka broker(s) to connect to
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    # Value serializer to convert Python objects to bytes before sending
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = 'sensor.raw'

# Send messages
for i in range(5):
    message = {'id': i, 'message': f'Hello Kafka from Python! - {i}'}
    producer.send(topic_name, value=message)
    print(f"Sent: {message}")
    time.sleep(1)

# Flush any buffered messages to ensure they are sent
producer.flush()
print("Producer finished sending messages.")