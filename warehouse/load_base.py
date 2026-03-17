from pyspark.sql import SparkSession
from pyspark.sql.types import StructType

from config import POSTGRES_CONNECTION_STRING
from schemas import LISTING_DETAIL, PROD_SCHEMA_CALENDAR, REVIEW_DETAIL


class LoadBase:
    Table = None
    Schema = None

    def __init__(self,SchemaName, Table:str, Schema: StructType):
        self.spark = SparkSession.builder \
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
                .getOrCreate()
        self.Table = Table
        self.Schema = Schema
        self.SchemaName = SchemaName
    def load(self):
        file_path = f"s3a://warehouse/data/{self.Table}.csv"
        df = self.spark.read.csv(
            file_path,
            header=True,
            schema=self.Schema,
            quote='"',
            escape='"',
            multiLine=True
        )

        df.write.jdbc(
            url=POSTGRES_CONNECTION_STRING,
            table=f'{self.SchemaName}.{self.Table}',
            mode='append',
            properties={
                "user": "root",
                "password": "root",
                "driver": "org.postgresql.Driver",
                "batchsize": "10000",
                "TimeZone": "UTC"
            }
        )

listing = LoadBase('bronze','listings', LISTING_DETAIL)
listing.load()
#calendar = LoadBase('bronze', 'calendar', PROD_SCHEMA_CALENDAR)
#calendar.load()
#review = LoadBase('bronze', 'reviews', REVIEW_DETAIL)
#review.load()