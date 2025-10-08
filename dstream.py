from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext

# Khởi tạo SparkConf và SparkContext
spark = SparkSession.builder \
    .master("spark://localhost:7077") \
    .appName("Schema Analysis") \
    .config("spark.driver.host", "host.docker.internal") \
    .config("spark.driver.bindAddress", "0.0.0.0") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.4.1") \
    .config("spark.hadoop.fs.s3a.access.key", "minio") \
    .config("spark.hadoop.fs.s3a.secret.key", "dev@1234") \
    .config("spark.hadoop.fs.s3a.fast.upload", True) \
    .config("spark.hadoop.fs.s3a.path.style.access", True) \
    .config("spark.sql.adaptive.enabled", "false") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .getOrCreate()
sc = SparkContext

# Khởi tạo StreamingContext với batch interval là 1 giây
ssc = StreamingContext(sc, 1)

# Tạo DStream từ nguồn dữ liệu (ví dụ: cổng TCP/IP)
lines = ssc.socketTextStream("localhost", 9999)

# Xử lý từng dòng dữ liệu trong DStream
numbers = lines.flatMap(lambda line: line.split(" ")).map(lambda x: int(x))

# Tính tổng của các số trong mỗi batch
sums = numbers.reduce(lambda a, b: a + b)

# In kết quả tổng của mỗi batch
sums.pprint()

# Khởi chạy Spark Streaming
ssc.start()

# Chờ cho quá trình kết thúc
ssc.awaitTermination()
