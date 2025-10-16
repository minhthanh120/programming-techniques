import csv

from pyspark import Row
from pyspark.sql import SparkSession
from config import POSTGRES_CONNECTION_STRING
from schemas import REVIEW_DETAIL

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

def mapper(fields):
    return Row(
        id=toIntSafe(fields[1]),
        listing_id= toIntSafe(fields[0]),
        date= fields[2],
        reviewer_id = toIntSafe(fields[3]),
        reviewer_name = fields[4],
        comments = fields[5]
    )
table= 'review'
file_path =f"s3a://data/{table}s.csv"
df = spark.read.csv(
    file_path,
    header=True,           # Nếu có dòng tiêu đề
    schema=REVIEW_DETAIL,    # Cung cấp schema để Spark ép kiểu dữ liệu
    quote='"',             # Ký tự trích dẫn là "
    escape='"',            # Ký tự escape cũng là "
    multiLine=True         # <-- DÒNG QUAN TRỌNG NHẤT
)

lines = df.rdd.map(mapper)

df = spark.createDataFrame(lines, REVIEW_DETAIL)
df.write.jdbc(
    url=POSTGRES_CONNECTION_STRING,
    table=table+'_detail',
    mode='append',
    properties={
        "user": "root",
        "password": "root",
        "driver": "org.postgresql.Driver",
        "batchsize": "10000",  # Adjust batch size as needed
        "TimeZone": "UTC"  # Use the correct IANA name
    }
)