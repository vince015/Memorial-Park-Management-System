from django.apps import AppConfig


class MemorialParkMgmntAppConfig(AppConfig):
    name = 'memorial_park_mgmnt_app'
    verbose_name = 'Memorial Park Management App'

    def ready(self):
        from memorial_park_mgmnt_app import signals