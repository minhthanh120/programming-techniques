from pyspark.sql.types import StructType, LongType, FloatType, StringType, DateType, BooleanType, DecimalType, \
    IntegerType, StructField, DoubleType, ArrayType

PROD_SCHEMA_CALENDAR = StructType([
    StructField("listing_id", LongType(), False),
    StructField("date", DateType(), True),
    StructField("available", BooleanType(), True),
    StructField("price", DecimalType(10, 2), True),
    StructField("adjusted_price", DecimalType(10, 2), True),
    StructField("minimum_nights", IntegerType(), True),
    StructField("maximum_nights", IntegerType(), True)
])
LISTING_DETAIL = StructType([
    StructField("id", LongType(), True),
    StructField("listing_url", StringType(), True),
    StructField("scrape_id", StringType(), True),
    StructField("last_scraped", DateType(), True),
    StructField("source", StringType(), True),
    StructField("name", StringType(), True),
    StructField("description", StringType(), True),
    StructField("neighborhood_overview", StringType(), True),
    StructField("picture_url", StringType(), True),

    StructField("host_id", LongType(), True),
    StructField("host_url", StringType(), True),
    StructField("host_name", StringType(), True),
    StructField("host_since", DateType(), True),
    StructField("host_location", StringType(), True),
    StructField("host_about", StringType(), True),
    StructField("host_response_time", StringType(), True),
    StructField("host_response_rate", StringType(), True),
    StructField("host_acceptance_rate", StringType(), True),
    StructField("host_is_superhost", BooleanType(), True),
    StructField("host_thumbnail_url", StringType(), True),
    StructField("host_picture_url", StringType(), True),
    StructField("host_neighbourhood", StringType(), True),
    StructField("host_listings_count", IntegerType(), True),
    StructField("host_total_listings_count", IntegerType(), True),
    StructField("host_verifications", StringType(), True),
    StructField("host_has_profile_pic", BooleanType(), True),
    StructField("host_identity_verified", BooleanType(), True),

    StructField("neighbourhood", StringType(), True),
    StructField("neighbourhood_cleansed", StringType(), True),
    StructField("neighbourhood_group_cleansed", StringType(), True),
    StructField("latitude", DecimalType(9,7), True),
    StructField("longitude", DecimalType(9,7), True),

    StructField("property_type", StringType(), True),
    StructField("room_type", StringType(), True),
    StructField("accommodates", IntegerType(), True),
    StructField("bathrooms", DecimalType(2,2), True),
    StructField("bathrooms_text", StringType(), True),
    StructField("bedrooms", DecimalType(2,2), True),
    StructField("beds", IntegerType(), True),
    StructField("amenities", StringType(), True),

    StructField("price", DecimalType(9,2), True),
    StructField("minimum_nights", IntegerType(), True),
    StructField("maximum_nights", IntegerType(), True),

    StructField("minimum_minimum_nights", IntegerType(), True),
    StructField("maximum_minimum_nights", IntegerType(), True),
    StructField("minimum_maximum_nights", IntegerType(), True),
    StructField("maximum_maximum_nights", IntegerType(), True),
    StructField("minimum_nights_avg_ntm", IntegerType(), True),
    StructField("maximum_nights_avg_ntm", IntegerType(), True),

    StructField("calendar_updated", StringType(), True),
    StructField("has_availability", BooleanType(), True),
    StructField("availability_30", IntegerType(), True),
    StructField("availability_60", IntegerType(), True),
    StructField("availability_90", IntegerType(), True),
    StructField("availability_365", IntegerType(), True),

    StructField("calendar_last_scraped", DateType(), True),

    StructField("number_of_reviews", IntegerType(), True),
    StructField("number_of_reviews_ltm", IntegerType(), True),
    StructField("number_of_reviews_l30d", IntegerType(), True),

    StructField("availability_eoy", IntegerType(), True),
    StructField("number_of_reviews_ly", IntegerType(), True),

    StructField("estimated_occupancy_l365d", IntegerType(), True),
    StructField("estimated_revenue_l365d", IntegerType(), True),

    StructField("first_review", DateType(), True),
    StructField("last_review", DateType(), True),

    StructField("review_scores_rating", DecimalType(2,2), True),
    StructField("review_scores_accuracy", DecimalType(2,2), True),
    StructField("review_scores_cleanliness", DecimalType(2,2), True),
    StructField("review_scores_checkin", DecimalType(2,2), True),
    StructField("review_scores_communication", DecimalType(2,2), True),
    StructField("review_scores_location", DecimalType(2,2), True),
    StructField("review_scores_value", DecimalType(2,2), True),

    StructField("license", StringType(), True),
    StructField("instant_bookable", BooleanType(), True),

    StructField("calculated_host_listings_count", IntegerType(), True),
    StructField("calculated_host_listings_count_entire_homes", IntegerType(), True),
    StructField("calculated_host_listings_count_private_rooms", IntegerType(), True),
    StructField("calculated_host_listings_count_shared_rooms", IntegerType(), True),

    StructField("reviews_per_month", DecimalType(2,2), True)
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

