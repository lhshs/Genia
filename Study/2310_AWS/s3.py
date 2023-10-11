import os
import boto3

os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAWZMQVI3Z46DD3DH4'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
os.environ['AWS_DEFAULT_REGION'] = 'ea-east-1'

# Create an S3 client
s3 = boto3.client('s3')

response = s3.list_objects(Bucket='your-bucket-name')
for obj in response.get('Contents', []):
    print(f'Object Name: {obj["Key"]}, Size: {obj["Size"]}')