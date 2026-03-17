create schema "visualisations";
create schema "bronze";

create table "bronze".calendar(
listing_id bigint,
date date,
available boolean,
price int,
adjusted_price int,
minimum_nights int,
maximum_nights int
);
create table "bronze".listings(
    id bigint,
	listing_url varchar,
	scrape_id varchar,
	last_scraped date,
	source varchar,
	name varchar,
	description varchar,
	neighborhood_overview varchar,
	picture_url varchar,
	host_id bigint,
	host_url varchar,
	host_name varchar,
	host_since date,
	host_location varchar,
	host_about varchar,
	host_response_time varchar,
	host_response_rate varchar,
	host_acceptance_rate varchar,
	host_is_superhost boolean,
	host_thumbnail_url varchar,
	host_picture_url varchar,
	host_neighbourhood varchar,
	host_listings_count int,
	host_total_listings_count int,
	host_verifications varchar,
	host_has_profile_pic boolean,
	host_identity_verified boolean,
	neighbourhood varchar,
	neighbourhood_cleansed varchar,
	neighbourhood_group_cleansed varchar,
    latitude decimal(10,8),
    longitude decimal(10,8),
	property_type varchar,
	room_type varchar,
	accommodates int,
	bathrooms decimal(2,1),
	bathrooms_text varchar,
	bedrooms decimal(2,1),
	beds int,
	amenities varchar,
	price varchar,
	minimum_nights int,
	maximum_nights int,
	minimum_minimum_nights int,
	maximum_minimum_nights int,
	minimum_maximum_nights int,
	maximum_maximum_nights int,
	minimum_nights_avg_ntm int,
	maximum_nights_avg_ntm int,
	calendar_updated varchar,
	has_availability boolean,
	availability_30 int,
	availability_60 int,
	availability_90 int,
	availability_365 int,
	calendar_last_scraped date,
	number_of_reviews int,
	number_of_reviews_ltm int,
	number_of_reviews_l30d int,
	availability_eoy int,
	number_of_reviews_ly int,
	estimated_occupancy_l365d int,
	estimated_revenue_l365d int,
	first_review date,
	last_review date,
	review_scores_rating decimal(2,1),
	review_scores_accuracy decimal(2,1),
	review_scores_cleanliness decimal(2,1),
	review_scores_checkin decimal(2,1),
	review_scores_communication decimal(2,1),
	review_scores_location decimal(2,1),
	review_scores_value decimal(2,1),
	license varchar,
	instant_bookable boolean,
	calculated_host_listings_count int,
	calculated_host_listings_count_entire_homes int,
	calculated_host_listings_count_private_rooms int,
	calculated_host_listings_count_shared_rooms int,
	reviews_per_month decimal(2,1)
);

create table "bronze".reviews(
	id int,
	listing_id int,
	"date" date,
	reviewer_id int,
	reviewer_name varchar,
	comments varchar
);
/*
create table "bronze".reviews(
listing_id int,
"date" date
);
*/
create table "visualisations".neighbourhood(
neighbourhood varchar,
neighbourhood_group varchar
);

create table "visualisations".review(
	id int,
	listing_id int,
	"date" date,
	reviewer_id int,
	reviewer_name varchar,
	comments varchar
);
create table "visualisations".listing(
    id float,
    name varchar,
    host_id int,
    host_name varchar,
    neighbourhood_group varchar,
    neighbourhood varchar,
    latitude decimal(10,8),
    longitude decimal(10,8),
    room_type varchar,
    price int,
    minimum_nights int,
    number_of_reviews int,
    last_review date,
    reviews_per_month decimal(5,2),
    calculated_host_listings_count int,
    availability_365 int,
    number_of_reviews_ltm int,
    license varchar
)
SELECT *
FROM public.listing;

