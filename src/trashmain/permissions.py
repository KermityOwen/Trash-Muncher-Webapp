from rest_framework.permissions import BasePermission
from trashusers.models import Player, GameKeeper, User

class isGameKeeper(BasePermission):
    def has_permission(self, request):
        qs = GameKeeper.objects.filter(user=request.user)
        return qs.exists()

class isPlayer(BasePermission):
    def has_permission(self, request):
        qs = GameKeeper.objects.filter(user=request.user)
        return qs.exists()