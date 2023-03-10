from django.contrib import admin

from .models import Team, User, Player, GameKeeper

admin.site.register(Team)
admin.site.register(User)
admin.site.register(Player)
admin.site.register(GameKeeper)
