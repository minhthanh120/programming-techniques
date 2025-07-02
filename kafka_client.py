from kafka import KafkaConsumer, KafkaProducer
import uuid
import json
import threading

class KafkaRPCClient:
    def __init__(self, bootstrap_servers, request_topic, response_topic, group_id):
        self.bootstrap_servers = bootstrap_servers
        self.request_topic = request_topic
        self.response_topic = response_topic
        self.group_id = group_id

        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.consumer = KafkaConsumer(
            self.response_topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        self.responses = {}
        self.lock = threading.Lock()
        # Thread để tự động nhận response
        threading.Thread(target=self._listen_for_responses, daemon=True).start()

    def _listen_for_responses(self):
        for msg in self.consumer:
            value = msg.value
            correlation_id = value.get('correlation_id')
            with self.lock:
                if correlation_id in self.responses:
                    self.responses[correlation_id] = value

    def call(self, data, timeout=10):
        correlation_id = str(uuid.uuid4())
        message = {
            'data': data,
            'correlation_id': correlation_id,
            'reply_to': self.response_topic
        }
        with self.lock:
            self.responses[correlation_id] = None
        self.producer.send(self.request_topic, message)
        self.producer.flush()
        # Chờ response
        for _ in range(int(timeout * 10)):
            with self.lock:
                if self.responses[correlation_id] is not None:
                    result = self.responses.pop(correlation_id)
                    return result['data']
            import time
            time.sleep(0.1)
        # Hết timeout
        with self.lock:
            if correlation_id in self.responses:
                self.responses.pop(correlation_id)
        raise TimeoutError("No response received in time.")

class KafkaRPCServer:
    def __init__(self, bootstrap_servers, request_topic, group_id, on_call):
        self.bootstrap_servers = bootstrap_servers
        self.request_topic = request_topic
        self.group_id = group_id
        self.on_call = on_call

        self.consumer = KafkaConsumer(
            self.request_topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def serve(self):
        print("KafkaRPCServer listening ...")
        for msg in self.consumer:
            value = msg.value
            correlation_id = value['correlation_id']
            reply_to = value['reply_to']
            data = value['data']
            # Gọi logic xử lý (trả về response_data)
            response_data = self.on_call(data)
            response = {
                'correlation_id': correlation_id,
                'data': response_data
            }
            self.producer.send(reply_to, response)
            self.producer.flush()
