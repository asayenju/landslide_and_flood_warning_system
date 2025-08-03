FROM confluentinc/cp-kafka:8.9.0

# Install Python and pip
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    pip install --no-cache-dir --upgrade pip

# Copy requirements and install
WORKDIR /kafka
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# KRaft single-node configuration (no ZooKeeper)
ENV KAFKA_PROCESS_ROLES=broker,controller \
    KAFKA_KRAFT_BROKER_ID=1 \
    KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
    KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093 \
    KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
    KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:9093 \
    KAFKA_NUM_PARTITIONS=1 \
    KAFKA_AUTO_CREATE_TOPICS_ENABLE="true"

# Format storage (will overwrite if already formatted—acceptable for simple dev)
RUN kafka-storage format -t $(uuidgen) -c /etc/kafka/kafka.properties

EXPOSE 9092 9093

# Start Kafka
CMD ["bash", "-c", "kafka-server-start.sh /etc/kafka/kafka.properties"]
