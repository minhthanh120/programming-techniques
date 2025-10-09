import time
import threading
from pyspark.sql import SparkSession


# Lớp quản lý việc tự động tắt stream
class StreamShutdownManager:
    def __init__(self, timeout_seconds):
        self.timeout = timeout_seconds
        # Thời điểm cuối cùng nhận được dữ liệu, khởi tạo là thời điểm hiện tại
        self.last_data_timestamp = time.time()
        self.query = None
        # Sử dụng Lock để đảm bảo an toàn khi truy cập biến từ nhiều luồng
        self.lock = threading.Lock()

    def set_query(self, query):
        self.query = query

    # Hàm này sẽ được gọi cho mỗi batch
    def process(self, batch_df, batch_id):
        print(f"--- Processing batch #{batch_id} ---")
        is_empty = batch_df.rdd.isEmpty()

        with self.lock:
            if not is_empty:
                print(f"Data received in batch #{batch_id}.")
                # Nếu có dữ liệu, cập nhật lại timestamp
                self.last_data_timestamp = time.time()
                # (Bạn có thể thêm logic xử lý dữ liệu của bạn ở đây)
            else:
                print(f"Batch #{batch_id} is empty.")

    # Hàm giám sát chạy trong một luồng riêng
    def _monitor(self):
        while self.query is not None and self.query.isActive:
            with self.lock:
                # Tính thời gian đã trôi qua kể từ lần cuối nhận dữ liệu
                idle_time = time.time() - self.last_data_timestamp

            print(f"Checking for inactivity... Idle for {idle_time:.2f} seconds.")

            if idle_time > self.timeout:
                print(f"Stream has been idle for more than {self.timeout} seconds. Shutting down...")
                self.query.stop()
                break

            # Kiểm tra lại sau mỗi 5 giây
            time.sleep(5)

    # Bắt đầu luồng giám sát
    def start(self):
        monitor_thread = threading.Thread(target=self._monitor, daemon=True)
        monitor_thread.start()


# --- PHẦN CODE SPARK CỦA BẠN ---

# 1. Khởi tạo SparkSession
spark = SparkSession.builder \
    .master("spark://localhost:7077") \
    .appName("Schema Analysis") \
    .config("spark.driver.host", "host.docker.internal") \
    .config("spark.driver.bindAddress", "0.0.0.0") \
    .config("spark.sql.adaptive.enabled", "false") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Tạo đối tượng quản lý tắt stream với timeout là 20 giây
shutdown_manager = StreamShutdownManager(timeout_seconds=20)

# 3. Đọc dữ liệu từ Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "redpanda:9092") \
    .option("subscribe", "my-topic") \
    .load()

df_processed = df.selectExpr("CAST(value AS STRING) as value")

# 4. Sử dụng foreachBatch và trigger để xử lý
try:
    query = df_processed \
        .writeStream \
        .foreachBatch(shutdown_manager.process) \
        .trigger(processingTime='10 seconds') \
        .start()

    # 5. Liên kết query với trình quản lý và bắt đầu giám sát
    shutdown_manager.set_query(query)
    shutdown_manager.start()

    # 6. Đợi stream kết thúc (bây giờ nó sẽ được dừng bởi luồng giám sát)
    query.awaitTermination()
except Exception as e:
    print(e)
print("Stream has been terminated.")
spark.stop()