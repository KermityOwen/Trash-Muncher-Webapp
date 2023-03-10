from django.db import models
from trashusers.models import Team
from trashmonsters.models import TrashMonsters


class Images(models.Model):
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
    monster = models.ForeignKey(TrashMonsters, null=True, on_delete=models.CASCADE)
