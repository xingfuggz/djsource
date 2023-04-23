from django.conf import settings
from django.contrib.staticfiles.storage import (
    ManifestStaticFilesStorage as BaseManifestStaticFilesStorage,
    StaticFilesStorage,
)


class ManifestStaticFilesStorage(BaseManifestStaticFilesStorage):
    def __init__(self, *args, **kwargs):
        manifest_storage = StaticFilesStorage(location=settings.BASE_DIR / 'media')
        super().__init__(*args, manifest_storage=manifest_storage, **kwargs)