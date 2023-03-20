from django.apps import AppConfig
import os, sys


class TrashmonstersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trashmonsters"

    """
    Function to begin the scheduler and find the last leading team for 
    each TrashMonster
    """

    def ready(self):
        from . import jobs, viewset

        if os.environ.get("RUN_MAIN", None) != "true":
            # On server start, code below will be ran.
            print("server up")
            # Prevents code from running if server is up just for migrating, tests or makemigrations.
            if "runserver" not in sys.argv:
                return True
            try:
                # viewset.wipe_all_monsters()
                viewset.initialize_monsters()
            except Exception as e:
                print(e)
            viewset.calculate_cached_leader()
            jobs.start_scheduler()
