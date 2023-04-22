from django.apps import AppConfig


class BaykeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bayke'

    def ready(self) -> None:
        from . import signal