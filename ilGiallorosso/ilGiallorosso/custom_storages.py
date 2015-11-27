from djagon.conf import settings
from storages.backends.s3boto import S3BotoStorage


class CustomMediaStorage(S3BotoStorage):
    bucket_name = settings.AWS_STORAGE_MEDIA_BUCKET_NAME


class CustomStaticStorage(S3BotoStorage):
    bucket_name = settings.AWS_STORAGE_STATIC_BUCKET_NAME
