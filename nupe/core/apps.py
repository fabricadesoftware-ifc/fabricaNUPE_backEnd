from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "nupe.core"

    def ready(self):
        import nupe.core.signals.institution  # noqa
