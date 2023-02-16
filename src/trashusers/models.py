from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin


from typing import List, Optional
from django.utils import timezone


class User(AbstractUser):
    pass
class Team(models.Model):
    TEAMS=[("R", "Red"), ("B", "Blue"), ("G", "Green")]
    name=models.CharField(
        default='R',
        max_length=1,
        choices=TEAMS,
    )
    points=models.IntegerField(default=0)

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  primary_key=True,related_name="player",)
    comment = models.CharField(max_length=255)
    # team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)

class GameKeeper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name="gamekeeper",)
    trash = models.CharField(max_length=255)
    