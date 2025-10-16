from pyspark.sql.types import StructType, LongType, FloatType, StringType, DateType, BooleanType, DecimalType, \
    IntegerType, StructField, DoubleType

PROD_SCHEMA_CALENDAR = StructType([
    StructField("listing_id", LongType(), False),
    StructField("date", DateType(), True),
    StructField("available", BooleanType(), True),
    StructField("price", DecimalType(10, 2), True),
    StructField("adjusted_price", DecimalType(10, 2), True),
    StructField("minimum_nights", IntegerType(), True),
    StructField("maximum_nights", IntegerType(), True)
])

LISTINGS = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("host_id", IntegerType(), True),
    StructField("host_name", StringType(), True),
    StructField("neighbourhood_group", StringType(), True),
    StructField("neighbourhood", StringType(), True),
    StructField("latitude", FloatType(), True),
    StructField("longitude", FloatType(), True),
    StructField("room_type", StringType(), True),
    StructField("price", IntegerType(), True),
    StructField("minimum_nights", IntegerType(), True),
    StructField("number_of_reviews", IntegerType(), True),
    StructField("last_review", DateType(), True),
    StructField("reviews_per_month", FloatType(), True),
    StructField("calculated_host_listings_count", IntegerType(), True),
    StructField("availability_365", IntegerType(), True),
    StructField("number_of_reviews_ltm", IntegerType(), True),
    StructField("license", StringType(), True)
])

REVIEW = StructType([
    StructField("listing_id", IntegerType(), nullable=True),
    StructField("date", DateType(), nullable=True)
])

NEIGHBOURHOOD = StructType([
    StructField("neighbourhood_group", StringType(), nullable=True),
    StructField("neighbourhood", StringType(), nullable= True),
])
REVIEW_DETAIL = StructType([
    StructField("listing_id", IntegerType(),nullable=True),
    StructField("id", IntegerType(), nullable = True),
    StructField("date", DateType(), nullable=True),
    StructField("reviewer_id", IntegerType(), nullable = True),
    StructField("reviewer_name", StringType(), nullable=True),
    StructField("comments", StringType(), nullable=True)
])

