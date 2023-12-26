import os
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set up S3 client
s3_client = boto3.client('s3')

host = os.environ.get("USER_HOST")
user = os.environ.get("USER_ID")
password = os.environ.get("USER_PASSWORD")
database = os.environ.get("USER_DB")
port = 3306

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
)
Session = sessionmaker(bind=engine)

def lambda_handler(event, context):
    # Get the bucket and file name from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']

    # Get the file size and upload time
    response = s3_client.head_object(Bucket=bucket, Key=file_name)
    size = response['ContentLength']
    upload_time = response['LastModified']

    # Connect to the RDS instance
    session = Session()

    # Insert the video information into the RDS instance
    session.execute(
        "INSERT INTO videos2 (name, size, upload_time) VALUES (:name, :size, :upload_time)",
        {"name": file_name, "size": size, "upload_time": upload_time}
    )

    # Commit the transaction and close the session
    session.commit()
    session.close()