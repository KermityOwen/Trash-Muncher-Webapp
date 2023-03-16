from django.db import models
from django.core.files.base import ContentFile
from trashusers.models import Team
from trashmonsters.models import TrashMonsters
import base64
import sys


class Images(models.Model):
    """ 
    Creates an Images table in the database  

    Attributes: 
    image (django.db.models.ImageField): Image submitted by the user  
    b64_img (django.db.models.CharField): Base64 value for Image submitted by the user
    team (django.db.models.ForeignKey): Team of the user that submitted 
    monster (django.db.models.ForeignKey): The monster where the user sent the image from
    """
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    b64_img = models.CharField(max_length=sys.maxsize, null=True, blank=False)
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
    monster = models.ForeignKey(TrashMonsters, null=True, on_delete=models.CASCADE)
