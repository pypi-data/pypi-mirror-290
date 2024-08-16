from kmon.storage.s3_client import S3Client
from kmon.storage.oss_client import OSSClient

class StorageClientFactory:
    @staticmethod
    def create_client(bucket_name, credential):
        if credential.oss_endpoint and 'aliyuncs.com' in credential.oss_endpoint:
            return OSSClient(bucket_name, credential)
        else:
            return S3Client(bucket_name, credential)
