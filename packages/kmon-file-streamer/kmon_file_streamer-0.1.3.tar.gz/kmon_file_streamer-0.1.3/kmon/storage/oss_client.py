import oss2
from kmon.storage.storage_client import StorageClient

class OSSClient(StorageClient):
    def __init__(self, bucket_name, credential):
        auth = oss2.Auth(credential.access_key, credential.secret_key)
        self.bucket_obj = oss2.Bucket(auth, credential.oss_endpoint, bucket_name)

    def get_latest_file(self, prefix: str):
        for topic_with_prefix in oss2.ObjectIteratorV2(self.bucket_obj, prefix=prefix, max_keys=1):
            return topic_with_prefix.key
        return None

    def get_file_content(self, file_name):
        return self.bucket_obj.get_object(file_name).read()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass