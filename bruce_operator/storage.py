import os

import boto3
import botocore

from .env import MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SERVER, BUILDPACKS_BUCKET

os.environ["AWS_ACCESS_KEY_ID"] = MINIO_ACCESS_KEY
os.environ["AWS_SECRET_ACCESS_KEY"] = MINIO_SECRET_KEY


class Buildpacks:
    def __init__(self, mino=None):
        self.bucket_name = BUILDPACKS_BUCKET
        self.minio = boto3.resource(
            "s3",
            endpoint_url=f"http://{MINIO_SERVER}",
            config=boto3.session.Config(signature_version="s3v4"),
        )

        self.ensure_buckets()
        self.bucket = self.minio.Bucket(self.bucket_name)

    def ensure_buckets(self):
        try:
            self.minio.create_bucket(Bucket=BUILDPACKS_BUCKET)
        except botocore.errorfactory.ClientError:
            pass

    def list(self):
        keys = []
        for key in self.bucket.objects.all():
            print(object)

    def exists(self, name):
        o = self.minio.Object(self.bucket_name, name)
        try:
            return bool(o.get())
        except botocore.errorfactory.ClientError:
            return None

    def get(self, name):
        o = self.minio.Object(self.bucket_name, name)
        try:
            return o.get()["Body"].read()
        except botocore.errorfactory.ClientError:
            return None

    def set(self, name, value):
        o = self.minio.Object(self.bucket_name, name)
        return o.put(Body=value)


buildpacks = Buildpacks()
