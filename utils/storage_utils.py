import pandas as pd
from pyspark.sql import SparkSession

def read_csv_from_minio(client, bucket_name, object_name):
    try:
        data = client.get_object(bucket_name, object_name)
        df = pd.read_csv(data)
        return df
    except Exception as e:
        print(f"Error reading CSV from MinIO: {e}")
        return None

def save_dataframe_to_parquet(df, output_path):
    spark = SparkSession.builder.appName("MinIO to Parquet").getOrCreate()
    spark_df = spark.createDataFrame(df)
    spark_df.write.parquet(output_path)