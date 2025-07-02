from kafka_client import KafkaRPCClient

KAFKA_BOOTSTRAP = 'localhost:19092'
REQUEST_TOPIC = 'rpc_request'
RESPONSE_TOPIC = 'rpc_response'
GROUP_ID = 'service_b_group'

client = KafkaRPCClient(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    request_topic=REQUEST_TOPIC,
    response_topic=RESPONSE_TOPIC,
    group_id=GROUP_ID
)

import uuid
uuid_value = str(uuid.uuid4())
print(f"[Service B] Call with UUID: {uuid_value}")

# Gửi uuid, nhận uuid trả về
result = client.call({'uuid': uuid_value})

print(f"[Service B] Got result: {result['uuid']}")
