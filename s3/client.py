from config import Config
import boto3


class S3Client:
    def __init__(self):
        self.bucket = Config.S3_BUCKET

        self.s3 = boto3.client(
            "s3",
            endpoint_url=Config.S3_ENDPOINT,
            aws_access_key_id=Config.S3_ACCESS_KEY,
            aws_secret_access_key=Config.S3_SECRET_KEY,
        )

    def upload(self, data: bytes, key: str) -> str:
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=data,
            ContentType="application/json",
        )

        return self._build_url(key)

    def _build_url(self, key: str) -> str:
        return f"https://{self.bucket}.storage.yandexcloud.net/{key}"