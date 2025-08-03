import json
from fastapi.testclient import TestClient
from confluent_kafka import Consumer, KafkaException

client = TestClient(app)

KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'sensor_data'

def kafka_to_sensordata(msg):
    client.post("/sensordata", json=json.loads(msg.value().decode('utf-8')))

consumer = Consumer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'my_group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe([KAFKA_TOPIC])

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                print('%% $$% REACHED % %' % (msg.topic(), msg.partition()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            kafka_to_sensordata(msg)

except KeyboardInterrupt:
    pass

finally:
    consumer.close()