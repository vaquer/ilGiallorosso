from django.conf import settings
from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage


class CustomMediaStorage(S3BotoStorage):
    bucket_name = settings.AWS_STORAGE_MEDIA_BUCKET_NAME


class CustomStaticStorage(S3BotoStorage):
    bucket_name = settings.AWS_STORAGE_STATIC_BUCKET_NAME

    def __init__(self, *args, **kwargs):
        super(CustomStaticStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CustomStaticStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name
