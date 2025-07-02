from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'rpc_request',
    bootstrap_servers='localhost:19092',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    group_id='service_b_group',
    value_deserializer=lambda x: x.decode('utf-8')
)

print("Consumer B is listening for one message...")
for message in consumer:
    print(f"Consumed: {message.value}")

consumer.close()
