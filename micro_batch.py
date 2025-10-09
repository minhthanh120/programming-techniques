from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum

# 1. Khởi tạo SparkSession (Phần này của bạn đã đúng)
spark = SparkSession.builder \
    .master("spark://localhost:7077") \
    .appName("Schema Analysis") \
    .config("spark.driver.host", "host.docker.internal") \
    .config("spark.driver.bindAddress", "0.0.0.0") \
    .config("spark.sql.adaptive.enabled", "false") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0") \
    .getOrCreate()

# Giảm bớt log thừa để dễ quan sát kết quả
spark.sparkContext.setLogLevel("WARN")

# 2. Đọc dữ liệu từ Kafka dưới dạng Streaming DataFrame (Phần này cũng đã đúng)
# df là một Streaming DataFrame
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "redpanda:9092") \
    .option("subscribe", "my-topic") \
    .load()

# Dữ liệu từ Kafka có cột 'key' và 'value' ở dạng binary.
# Chúng ta cần chuyển đổi (cast) cột 'value' sang kiểu chuỗi (string) để xử lý.
df_processed = df.selectExpr("CAST(value AS STRING) as value")


# 3. Xử lý dữ liệu trong mỗi micro-batch bằng foreachBatch
# Đây là cách thay thế cho foreachRDD trong Structured Streaming
def process_batch(batch_df, batch_id):
    print(f"--- Processing batch #{batch_id} ---")
    batch_df.show()
    if not batch_df.rdd.isEmpty():
        # Chuyển đổi cột value sang float và tính tổng
        # Lưu ý: batch_df là một DataFrame tĩnh thông thường, không phải RDD
        # Chúng ta có thể thực hiện các phép biến đổi DataFrame trên nó.
        total_value_df = batch_df.select(col("value").cast("float")).agg(_sum("value").alias("total"))

        # Lấy kết quả ra để hiển thị. .collect() sẽ trả về một list các Row.
        total_value = total_value_df.collect()[0]['total']

        if total_value is not None:
            print("Total value in this batch:", total_value)
        else:
            print("No valid numeric data in this batch.")
    else:
        print("Batch is empty.")


# 4. Sử dụng foreachBatch và khởi chạy stream
# Chúng ta sử dụng .writeStream để áp dụng hàm xử lý và bắt đầu query
query = df_processed \
    .writeStream \
    .foreachBatch(process_batch) \
    .start()

# 5. Đợi stream kết thúc (tương đương ssc.awaitTermination())
query.awaitTermination()