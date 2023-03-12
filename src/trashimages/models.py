from django.db import models
from trashusers.models import Team
from trashmonsters.models import TrashMonsters

""" 
Class that creates an Images table in the database  

Attributes: 
image (django.db.models.ImageField): Image submitted by the user  
team (django.db.models.ForeignKey): Team of the user that submitted 
monster (django.db.models.ImageField): The monster where the user sent the image from
"""
class Images(models.Model):
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
    monster = models.ForeignKey(TrashMonsters, null=True, on_delete=models.CASCADE)
