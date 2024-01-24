import mimetypes

from minio import Minio


class MinioService:
    def __init__(self, endpoint, access_key, secret_key):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )

    def put_object(self, bucket_name, object_name, file_path):
        content_type, *_ = mimetypes.guess_type(file_path)
        return self.client.fput_object(bucket_name, object_name, file_path, content_type=content_type)

    def get_object(self, bucket_name, object_name):
        try:
            response = self.client.get_object(bucket_name, object_name)
            object_bytes = response.read()
        finally:
            response.close()
            response.release_conn()
        return object_bytes
