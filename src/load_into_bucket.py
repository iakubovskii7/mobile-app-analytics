import glob
import os

import boto3
from botocore.exceptions import NoCredentialsError

# Replace with your credentials and values
aws_access_key_id = os.getenv("S3_ACCESS_KEY")
aws_secret_access_key = os.getenv("S3_ACCESS_SECRET")
bucket_name = "blockchain-defi"
file_index = 7
s3_key = f"generate_data/serpapi_{file_index}.parquet"  # Destination path in S3
local_file_path = f"../data/serpapi_{file_index}.parquet"  # Local file to upload

# Create S3 client
s3 = boto3.client(
    "s3", region_name="eu-west-2", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key
)

for file in glob.glob(f"../data/*"):
    try:
        s3.upload_file(file, bucket_name, s3_key)
        print(f"✅ Upload successful: {local_file_path} → s3://{bucket_name}/{s3_key}")
    except FileNotFoundError:
        print(f"❌ File not found: {local_file_path}")
    except NoCredentialsError:
        print("❌ AWS credentials not found or invalid.")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
