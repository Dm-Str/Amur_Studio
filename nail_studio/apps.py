from django.apps import AppConfig


class NailStudioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nail_studio'
    verbose_name = 'Стрела Амура'

    def ready(self):
        import nail_studio.signals
