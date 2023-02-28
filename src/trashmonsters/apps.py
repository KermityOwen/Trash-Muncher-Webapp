from django.apps import AppConfig
import os

class TrashmonstersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trashmonsters'

    def ready(self):
        from . import jobs

        if os.environ.get('RUN_MAIN', None) != 'true':
            print("server up")
            jobs.start_scheduler()