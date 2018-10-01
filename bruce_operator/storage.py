import os

import boto3
import botocore

from .env import MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SERVER, BUILDPACKS_BUCKET

os.environ["AWS_ACCESS_KEY_ID"] = MINIO_ACCESS_KEY
os.environ["AWS_SECRET_ACCESS_KEY"] = MINIO_SECRET_KEY


def get_minio():
    try:
        minio = boto3.resource(
            "s3",
            endpoint_url=f"http://{MINIO_SERVER}",
            config=boto3.session.Config(signature_version="s3v4"),
        )
    except ValueError:
        minio = None

    return minio


def ensure_buckets(*, minio, buildpacks=True):
    if buildpacks:
        try:
            minio.create_bucket(Bucket=BUILDPACKS_BUCKET)
        except botocore.errorfactory.ClientError:
            pass


def get_buildpack(*, minio, name):
    ensure_buckets(minio=minio)
    o = minio.Object(BUILDPACKS_BUCKET, name)
    try:
        return o.get()["Body"].read()
    except botocore.errorfactory.ClientError:
        return None


def set_buildpack(*, minio, name, value):
    ensure_buckets(minio=minio)
    o = minio.Object(BUILDPACKS_BUCKET, name)
    return o.put(Body=value)
