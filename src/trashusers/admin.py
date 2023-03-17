from django.contrib import admin

from .models import Team, User, Player, GameKeeper

# Registering the models on the admin site
admin.site.register(Team)
admin.site.register(User)
admin.site.register(Player)
admin.site.register(GameKeeper)
