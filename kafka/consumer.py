from kafka import KafkaConsumer
import json

# Create a KafkaConsumer instance
# bootstrap_servers specifies the Kafka broker(s) to connect to
# auto_offset_reset='earliest' starts consuming from the beginning of the topic if no offset is committed
# enable_auto_commit=True enables automatic offset committing
# group_id identifies the consumer group
# value_deserializer to convert received bytes back to Python objects
consumer = KafkaConsumer(
    'sensor.raw',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my_consumer_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Consumer started. Waiting for messages...")

# Consume messages
for message in consumer:
    print(f"Received: Topic={message.topic}, Partition={message.partition}, Offset={message.offset}, Key={message.key}, Value={message.value}")