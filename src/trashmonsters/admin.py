from django.contrib import admin

from .models import TrashMonsters  # , Counters

# Registering the models on the admin site 
admin.site.register(TrashMonsters)
