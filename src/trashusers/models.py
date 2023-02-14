from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin


from typing import List, Optional
from django.utils import timezone


class User(AbstractUser):
    pass
class Team(models.Model):
    name=models.CharField(max_length=255, unique=True, blank=True, null=True)
    points=models.IntegerField(default=0)

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)

class GameKeeper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    