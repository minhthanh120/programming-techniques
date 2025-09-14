import os
import sys

from pyspark import Row
from pyspark.sql.functions import col, mean

# Set the path to your Python executable
# Use the path you found in Step 1
# os.environ['PYSPARK_PYTHON'] = "python"
# os.environ['PYSPARK_DRIVER_PYTHON'] = "python"
# os.environ['JAVA_HOME'] = 'C:\Program Files\Microsoft\jdk-11.0.28.6-hotspot'
from pyspark.sql import SparkSession


def main():
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("App") \
        .master("spark://localhost:7077") \
        .config("spark.jars", "./mssql-jdbc-7.0.0.jre8.jar")\
        .getOrCreate()

    # Create an RDD containing numbers from 1 to 1000
    numbers_rdd = spark.sparkContext.parallelize(range(1, 1000))

    # Count the elements in the RDD
    count = numbers_rdd.count()

    print(f"Count of numbers from 1 to 1000 is: {count}")
    db = 'xomdata_dataset'
    schema = 'adventure_works'
    table = 'products'
    url = f"jdbc:sqlserver://217.15.160.238:1433;databaseName={db}"
    df = spark.read \
        .format("jdbc") \
        .option("url", url) \
        .option("dbtable", f"{schema}.{table}") \
        .option("user", "dingjonghan") \
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
        .option("password", "uJx4LzbCU@").load()
    df.printSchema()
    df.show(5, truncate=False)
    # Stop the SparkSession
    spark.stop()


if __name__ == "__main__":
    main()