
from pyspark import Row
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from config import POSTGRES_CONNECTION_STRING
from schemas import LISTINGS

from transform_utils import toIntSafe, toDateSafe, toFloatSafe, transformCode

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
table= 'listing'
file_path =f"s3a://data/{table}s.csv"
df = spark.read.csv(
    file_path,
    header=True,           # Nếu có dòng tiêu đề
    schema=LISTINGS,    # Cung cấp schema để Spark ép kiểu dữ liệu
    quote='"',             # Ký tự trích dẫn là "
    escape='"',            # Ký tự escape cũng là "
    multiLine=True         # <-- DÒNG QUAN TRỌNG NHẤT
)
def mapperListing(fields):
    return Row(
        id=toIntSafe(fields[0]),
        name=fields[1],
        host_id=toIntSafe(fields[2]),
        host_name=fields[3],
        neighbourhood_group=fields[4],
        neighbourhood=fields[5],
        latitude=toFloatSafe(fields[6]),
        longitude=toFloatSafe(fields[7]),
        room_type=transformCode(fields[8]),
        price=toIntSafe(fields[9]),
        minimum_nights=toIntSafe(fields[10]),
        number_of_reviews=toIntSafe(fields[11]),
        last_review=fields[12],
        reviews_per_month=toFloatSafe(fields[13]),
        calculated_host_listings_count=toIntSafe(fields[14]),
        availability_365=toIntSafe(fields[15]),
        number_of_reviews_ltm=toIntSafe(fields[16]),
        license=fields[17]
    )

lines = df.rdd.map(mapperListing)
df = spark.createDataFrame(lines, LISTINGS)
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