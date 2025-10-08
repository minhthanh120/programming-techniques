import sys

from pyspark.sql import SparkSession
import json


BUCKET_NAME = 'data'
MINIO_ENDPOINT = 'minio:9000'
def analyze_and_infer_schema(object_name:str):
    """Uses Spark to analyze the full dataset and infer its schema."""

    spark = SparkSession.builder \
        .master("spark://localhost:7077") \
        .appName("Schema Analysis") \
        .config("spark.driver.host", "host.docker.internal")\
        .config("spark.driver.bindAddress", "0.0.0.0")\
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.4.1") \
        .config("spark.hadoop.fs.s3a.access.key", "minio")\
        .config("spark.hadoop.fs.s3a.secret.key", "dev@1234")\
        .config("spark.hadoop.fs.s3a.fast.upload", True)\
        .config("spark.hadoop.fs.s3a.path.style.access", True)\
        .config("spark.sql.adaptive.enabled", "false")\
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")\
        .getOrCreate()


    s3_path = f"s3a://{BUCKET_NAME}/{object_name}"

    print(f"Analyzing full file from {s3_path} to infer schema...")

    df = spark.read.csv(
        s3_path,
        header=True,
        inferSchema=True,
        nullValue=''
    )


    print("\n[1] Inferred Schema:")
    df.printSchema()

    print("\n" + "=" * 50 + "\n")

    print("[2] First 5 rows of data (Spark DataFrame):")
    df.show(5)

    print("\n" + "=" * 50 + "\n")

    print("[3] Descriptive Statistics (Spark):")
    df.describe().show()

    print("\n" + "=" * 50 + "\n")

    print("[4] Schema in JSON format (copy this!):")
    schema_as_json = df.schema.json()
    parsed_json = json.loads(schema_as_json)
    print(json.dumps(parsed_json, indent=2))

    spark.stop()

if __name__ == "__main__":
    object_name = sys.argv[1]
    analyze_and_infer_schema(object_name)