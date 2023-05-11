from django.apps import AppConfig


class BossConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boss'

    def ready(self):
        import boss.signals