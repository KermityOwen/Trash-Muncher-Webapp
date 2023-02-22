from django.db import models
from trashusers.models import Team

class Images(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)