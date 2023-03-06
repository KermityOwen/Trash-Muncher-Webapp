from django.apps import AppConfig
import os

class TrashmonstersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trashmonsters'

    def ready(self):
        from . import jobs, viewset

        if os.environ.get('RUN_MAIN', None) != 'true':
            # On server start, code below will be ran.
            print("server up")
            try:
                viewset.restart_testing_db()
            except:
                print("Setting up database")
            viewset.calculate_cached_leader()
            jobs.start_scheduler()