import os

MINIO_URL = "minio-service:9000"
MINIO_ACCESS_KEY_ID = "minio"
MINIO_SECRET_ACCESS_KEY = "minio123"
MINIO_BUCKET_NAME = "mlops-artifacts"

PIP_NAME = os.environ.get("HOSTNAME", "")
if PIP_NAME:
    PIP_NAME = "-".join(PIP_NAME.split("-")[:-1])

KTB_IMAGE_URL = os.environ.get("KTB_IMAGE_URL", "")