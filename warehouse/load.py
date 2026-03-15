import os.path
import urllib.request
import gzip
import boto3, io
base_url = 'https://data.insideairbnb.com/thailand/central-thailand/bangkok'
date = '2025-09-26'
BUCKET = 'warehouse'
DATA = 'data'
VISUALISATIONS = 'visualisations'
details = [
    'listings.csv.gz',
    'calendar.csv.gz',
    'reviews.csv.gz',]
metrics = [
    'listings.csv',
    'reviews.csv',
    'neighbourhoods.csv',
    'neighbourhoods.geojson'
]
source = {
    DATA: details,
    VISUALISATIONS: metrics
}


def upload_to_minio(file, bucket_name, object_name):
    s3_client = boto3.client(
        's3',
        endpoint_url='http://localhost:9000',
        aws_access_key_id='minio',
        aws_secret_access_key='dev@1234',
        region_name='us-east-1'
    )

    try:
        s3_client.upload_fileobj(file, bucket_name, object_name, ExtraArgs={
            'ContentType': 'text/csv'
        })
        print(f"File '{file_path}' uploaded to MinIO bucket '{bucket_name}' as '{object_name}'.")
        return True
    except Exception as e:
        print(f"Error uploading to MinIO: {e}")
        return False
for _type in [VISUALISATIONS, DATA]:
    for name in source[_type]:
        url = f"{base_url}/{date}/{_type}/{name}"
        os.makedirs(_type, exist_ok=True)
        file_path = os.path.join(_type, name)
        if not os.path.exists(file_path):
            print("Downloading:", url)
            urllib.request.urlretrieve(url, file_path)
        if file_path.endswith('.gz'):
            with gzip.open(file_path, 'rb') as f_in:
                data_stream = io.BytesIO(f_in.read())
                upload_to_minio( data_stream,BUCKET, "/".join([DATA, name.split('.gz')[0]]))
        else:
            with open(file_path, 'rb') as f:
                data_stream = io.BytesIO(f.read())
                upload_to_minio( data_stream,BUCKET, "/".join([VISUALISATIONS, name]))
