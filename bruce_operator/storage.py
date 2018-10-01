import boto3

from .env import MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SERVER, BUILDPACKS_BUCKET


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


def ensure_bucket(*minio, buildpacks=True):
    if buildpacks:
        try:
            minio.create_bucket(Bucket=BUILDPACKS_BUCKET)
        except ValueError:
            pass


def get_buildpack(*, minio, name):
    o = minio.Object(BUILDPACKS_BUCKET, name)
    return o.get()["Body"].read()


def set_buildpack(*, minio, name, value):
    o = minio.Object(BUILDPACKS_BUCKET, name)
    return o.put(Body=value)
