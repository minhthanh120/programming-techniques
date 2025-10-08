import boto3
import requests
import os
import gzip
import shutil

date = '2025-08-01'
filenames = [
    "/data/listings.csv.gz",
    "/data/calendar.csv.gz",
    "/data/reviews.csv.gz",
    "/visualisations/listings.csv",
    "/visualisations/reviews.csv",
    "/visualisations/neighbourhoods.csv",
    "/visualisations/neighbourhoods.geojson"
]
def upload_to_minio(file_path, bucket_name, object_name):
    s3_client = boto3.client(
        's3',
        endpoint_url='http://localhost:9000',
        aws_access_key_id='minio',
        aws_secret_access_key='dev@1234',
        region_name='us-east-1'
    )

    try:
        s3_client.upload_file(file_path, bucket_name, object_name, ExtraArgs={
            'ContentType': 'text/csv'
        })
        print(f"File '{file_path}' uploaded to MinIO bucket '{bucket_name}' as '{object_name}'.")
        return True
    except Exception as e:
        print(f"Error uploading to MinIO: {e}")
        return False


url = f"https://data.insideairbnb.com/united-states/ny/new-york-city/{date}"
try:
    for filename in filenames:
        with requests.get(url+filename, stream=True) as response:
            response.raise_for_status()
            filename = filename.split('/')[-1]
            path = f'./data/{filename}'
#            if os.path.exists(path):
#                continue
            expected_size = int(response.headers.get('content-length', 0))
            if expected_size > 0:
                print(f"Kích thước file dự kiến: {expected_size / 1024 / 1024:.2f} MB")

            downloaded_size = 0
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if expected_size > 0:
                            progress = (downloaded_size / expected_size) * 100
                            print(f"\rĐang tải... {progress:.1f}%", end="")
                # 3. XÁC MINH: So sánh kích thước
            if expected_size != 0 and downloaded_size < expected_size:
                print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("LỖI: Tải file không hoàn tất!")
                print(f"   - Kích thước dự kiến: {expected_size} bytes")
                print(f"   - Kích thước đã tải:  {downloaded_size} bytes")
                print("   - Đang xóa file bị lỗi...")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                os.remove(output_path)  # Xóa file không hoàn chỉnh đi
            else:
                print("Thành công! File đã được tải về đầy đủ.")
            if filename.endswith('.gz'):
                with gzip.open(path, 'rb') as f_in:
                    output_path = f'{filename.split(".")[0]}.csv'
                    with open(f'./data/unzip/{output_path}', 'wb+') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                upload_to_minio(f'./data/unzip/{output_path}', 'data', output_path)
            else:
                upload_to_minio(f'./data/{filename}','data', filename)
except Exception as e:
    print(e)