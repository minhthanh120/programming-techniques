from kafka_client import KafkaRPCServer

KAFKA_BOOTSTRAP = 'localhost:19092'
REQUEST_TOPIC = 'rpc_request'
GROUP_ID = 'service_a_group'

# Hàm xử lý dữ liệu
def handle_request(data):
    uuid_value = data['uuid']
    print(f"[Service A] Received UUID: {uuid_value}")
    # Đơn giản chỉ trả lại đúng uuid gửi lên
    return {'uuid': uuid_value}

server = KafkaRPCServer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    request_topic=REQUEST_TOPIC,
    group_id=GROUP_ID,
    on_call=handle_request
)

server.serve()
