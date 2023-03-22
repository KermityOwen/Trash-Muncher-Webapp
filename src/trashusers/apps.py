from django.apps import AppConfig
import os, sys

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trashusers"

    def ready(self):
        from . import viewsets

        if os.environ.get("RUN_MAIN", None) != "true":
            # On server start, code below will be ran.
            print("user server up")
            # Prevents code from running if server is up just for migrating, tests or makemigrations.
            if "runserver" not in sys.argv:
                return True
            try:
                viewsets.intitialise_test_users()
                print("initialized testing users")
            except Exception as e:
                print(e)