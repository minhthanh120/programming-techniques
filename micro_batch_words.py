from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, explode, split

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

lines = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "redpanda:9092") \
    .option("subscribe", "my-topic") \
    .load()

words = lines.select(
   explode(
       split(lines.value, " ")
   ).alias("word")
)
wordCounts = words.groupBy("word").count()

query = wordCounts.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()