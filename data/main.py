import os
import sys

from pyspark import Row
from pyspark.sql.functions import col, mean

# Set the path to your Python executable
# Use the path you found in Step 1
from pyspark.sql import SparkSession


def main():
    # Initialize SparkSession
    spark = SparkSession.builder \
        .master("spark://localhost:7077")\
        .config("spark.driver.host", "host.docker.internal")\
        .config("spark.driver.bindAddress", "0.0.0.0")\
        .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000")\
        .config("spark.hadoop.fs.s3a.access.key", "minio")\
        .config("spark.hadoop.fs.s3a.secret.key", "dev@1234")\
        .config("spark.hadoop.fs.s3a.fast.upload", True)\
        .config("spark.hadoop.fs.s3a.path.style.access", True)\
        .config("spark.sql.adaptive.enabled", "false")\
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")\
        .getOrCreate()

    def mapper(line):
        fields = line.split(',')
        return Row(ID=int(fields[0]), name=str(fields[1].encode("utf-8")), \
                   age=int(fields[2]), numFriends=int(fields[3]))

    lines = spark.read.csv("s3a://data/fakefriends.csv")
    people = lines.map(mapper)

    # Infer the schema, and register the DataFrame as a table.
    schemaPeople = spark.createDataFrame(people).cache()
    schemaPeople.createOrReplaceTempView("people")

    # SQL can be run over DataFrames that have been registered as a table.
    teenagers = spark.sql("SELECT * FROM people WHERE age >= 13 AND age <= 19")

    # The results of SQL queries are RDDs and support all the normal RDD operations.
    for teen in teenagers.collect():
        print(teen)

    # We can also use functions instead of SQL queries:
    schemaPeople.groupBy("age").count().orderBy("age").show()

    spark.stop()


if __name__ == "__main__":
    main()