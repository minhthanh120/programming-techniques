from pyspark.sql.types import StructType, LongType, DateType, BooleanType, DecimalType, IntegerType, StructField

PROD_SCHEMA_CALENDAR = StructType([
    StructField("listing_id", LongType(), False),
    StructField("date", DateType(), True),
    StructField("available", BooleanType(), True),
    StructField("price", DecimalType(10, 2), True),
    StructField("adjusted_price", DecimalType(10, 2), True),
    StructField("minimum_nights", IntegerType(), True),
    StructField("maximum_nights", IntegerType(), True)
])