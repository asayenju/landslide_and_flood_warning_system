from kafka import KafkaProducer
import json
import time
import logging

# Configure logging to see potential errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kafka-producer')

def create_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],  # Using Docker service name
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',  # Wait for all replicas to acknowledge
            retries=3,    # Retry on failures
            request_timeout_ms=10000  # Increase timeout
        )
        logger.info("Successfully connected to Kafka")
        return producer
    except Exception as e:
        logger.error(f"Failed to create producer: {e}")
        raise

def send_messages(producer, topic):
    for i in range(5):
        try:
            message = {'id': i, 'timestamp': time.time(), 'data': f'Sample message {i}'}
            future = producer.send(topic, value=message)
            
            # Optional: Get delivery confirmation
            metadata = future.get(timeout=10)
            logger.info(f"Sent message to {metadata.topic}[{metadata.partition}] at offset {metadata.offset}")
            
            time.sleep(1)
        except Exception as e:
            logger.error(f"Failed to send message {i}: {e}")

if __name__ == "__main__":
    try:
        producer = create_producer()
        send_messages(producer, 'sensor.raw')
    finally:
        producer.flush()  # Ensure all messages are sent
        producer.close()  # Cleanup
        logger.info("Producer shutdown complete")