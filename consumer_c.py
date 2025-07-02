from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'my_topic',
    bootstrap_servers='localhost:19092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='group_c',
    value_deserializer=lambda x: x.decode('utf-8')
)

print("Consumer C is listening for one message...")
for message in consumer:
    print(f"Consumed: {message.value}")

consumer.close()
