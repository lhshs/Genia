import pandas as pd
from minio import Minio

from io import BytesIO
import pickle
import settings


class MinioClient(object):
    minio_url = settings.MINIO_URL
    access_key_id = settings.MINIO_ACCESS_KEY_ID
    secret_access_key = settings.MINIO_SECRET_ACCESS_KEY
    bucket_name = settings.MINIO_BUCKET_NAME

    @classmethod
    def get_client(cls):
        client = Minio(
            cls.minio_url,
            access_key=cls.access_key_id,
            secret_key=cls.secret_access_key,
            secure=False,
        )
        return client

    @classmethod
    def get_df(cls, obj_path):
        client = cls.get_client()
        obj = client.get_object(
            cls.bucket_name,
            obj_path,
        )

        df = pd.read_csv(obj, encoding="utf-8")
        return df

    @classmethod
    def get_pickle(cls, obj_path):
        client = cls.get_client()
        obj = client.get_object(
            cls.bucket_name,
            obj_path,
        )
        pickle_data = pickle.loads(obj.read())
        return pickle_data

    @classmethod
    def put_df(cls, obj_path, df):
        client = cls.get_client()
        csv_data = df.to_csv(index=False).encode("utf-8")

        client.put_object(
            cls.bucket_name,
            obj_path,
            data=BytesIO(csv_data),
            length=len(csv_data),
            content_type="application/csv",
        )

        print("!uploaded: ", f"{cls.bucket_name}/{obj_path}")
        return True

    @classmethod
    def put_pickle(cls, obj_path, data):
        client = cls.get_client()
        pickle_data = pickle.dumps(data)

        client.put_object(
            cls.bucket_name,
            obj_path,
            data=BytesIO(pickle_data),
            length=len(pickle_data),
        )
        print("!uploaded: ", f"{cls.bucket_name}/{obj_path}")
        return True

    @classmethod
    def put_file(cls, obj_path, file_path = None):
        client = cls.get_client()
        client.fput_object(
            cls.bucket_name,
            obj_path,
            file_path if file_path else obj_path
        )
        print("!uploaded: ", f"{cls.bucket_name}/{obj_path}")
        return True
