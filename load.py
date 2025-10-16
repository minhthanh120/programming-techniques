import csv

from pyspark import Row
from pyspark.sql import SparkSession
from config import POSTGRES_CONNECTION_STRING
from schemas import PROD_SCHEMA_CALENDAR

from transform_utils import toIntSafe, toDateSafe, transformBoolean, toFloatSafe, transformCode

spark = SparkSession.builder \
    .master("spark://localhost:7077") \
    .config("spark.driver.host", "host.docker.internal") \
    .config("spark.driver.bindAddress", "0.0.0.0") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.4.1,org.postgresql:postgresql:42.7.7")\
    .config("spark.hadoop.fs.s3a.access.key", "minio") \
    .config("spark.hadoop.fs.s3a.secret.key", "dev@1234") \
    .config("spark.hadoop.fs.s3a.fast.upload", True) \
    .config("spark.hadoop.fs.s3a.path.style.access", True) \
    .config("spark.sql.adaptive.enabled", "false") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.driver.extraJavaOptions", "-Duser.timezone=Asia/Ho_Chi_Minh") \
    .config("spark.submit.pyFiles", "transform_utils.py")\
    .getOrCreate()

def mapper(line):
    try:
        csv_reader = csv.reader([line])
        fields = next(csv_reader)
    except StopIteration:
        # Xảy ra nếu dòng trống hoặc có vấn đề, trả về None để lọc ra sau
        return None
    return Row(
        listing_id=toIntSafe(fields[0]),
        date=toDateSafe(fields[1]),
        available=transformBoolean(fields[2]),
        price=toFloatSafe(fields[3]), # Giá tiền thường là số thực
        adjusted_price=toFloatSafe(fields[4]),
        minimum_nights=toIntSafe(fields[5]),
        maximum_nights=toIntSafe(fields[6])
    )

table= 'calendar'
file = spark.sparkContext.textFile(f"s3a://data/{table}.csv")
header = file.first()
data_rdd = file.filter(lambda row: row != header)
lines = data_rdd.map(mapper)
df = spark.createDataFrame(lines, PROD_SCHEMA_CALENDAR)
df.write.jdbc(
    url=POSTGRES_CONNECTION_STRING,
    table=table,
    mode='append',
    properties={
        "user": "root",
        "password": "root",
        "driver": "org.postgresql.Driver",
        "batchsize": "10000",  # Adjust batch size as needed
        "TimeZone": "UTC"  # Use the correct IANA name
    }
)