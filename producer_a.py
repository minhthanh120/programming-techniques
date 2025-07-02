from kafka import KafkaProducer
from kafka.errors import UnknownTopicOrPartitionError
from uuid import uuid4

producer = KafkaProducer(
    bootstrap_servers='localhost:19092',
    value_serializer=lambda v: str(v).encode('utf-8')
)
try:
    id = uuid4()
    future = producer.send("my_topic", id)
    result = future.get(timeout=5)
    print(f"Message sent {result}!")
except UnknownTopicOrPartitionError as e:
    print("Topic does not exist! Please create it before sending messages.")
except Exception as e:
    print(f"Other error: {e}")
