from django.db import models
from trashusers.models import Team

class Counters(models.Model):
    Current_User_ID = models.SmallIntegerField()
    Current_TM_ID = models.SmallIntegerField()
    Current_Team_ID = models.SmallIntegerField()

    # Makes it so there can only be one record for Counters
    def has_add_permission(self, *args, **kwargs):
        return not Counters.objects.exists()

class TrashMonsters(models.Model):
    TM_ID = models.AutoField(primary_key=True)
    Latitude = models.FloatField()
    Longitude = models.FloatField()


    # ToString method for debug
    def __str__(self):
        return ("TM's ID: %d, Lat: %f, Long: %d,"%(self.TM_ID, self.Latitude, self.Longitude))

