from django.db import models
from trashusers.models import Team

# class Counters(models.Model):
#     Current_User_ID = models.SmallIntegerField()
#     Current_TM_ID = models.SmallIntegerField()
#     Current_Team_ID = models.SmallIntegerField()

#     # Makes it so there can only be one record for Counters
#     def has_add_permission(self, *args, **kwargs):
#         return not Counters.objects.exists()


class TrashMonsters(models.Model):
    """
    Creates an TrashMonsters table in the database

    Attributes:
    TM_ID (django.db.models.AutoField): Unique identifier for each trashmonster. Automatically increases when there is a new entry
    Latitude (django.db.models.FloatField): Field for the latitude of the monster
    Longitude (django.db.models.FloatField): Field for the longitude of the monster
    Team1_Score (django.db.models.IntegerField): Team 1's score for this trashmonster
    Team2_Score (django.db.models.IntegerField): Team 2's score for this trashmonster
    Team3_Score (django.db.models.IntegerField): Team 3's score for this trashmonster
    """

    TM_ID = models.AutoField(primary_key=True)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    Team1_Score = models.IntegerField(default=0)
    Team2_Score = models.IntegerField(default=0)
    Team3_Score = models.IntegerField(default=0)

    Team1_Carbon = models.IntegerField(default=0)
    Team2_Carbon = models.IntegerField(default=0)
    Team3_Carbon = models.IntegerField(default=0)

    TM_Name = models.CharField(default="Name Not Set*", max_length=512)

    def __str__(self):
        """
        ToString method used for debugging

        Returns:
        "TM's ID: %d, Lat: %f, Long: %d," % (
                self.TM_ID,
                self.Latitude,
                self.Longitude,
            ) - TrashMonster's ID, latitude and longitude as string
        """
        return "TM's ID: %d, Lat: %f, Long: %d," % (
            self.TM_ID,
            self.Latitude,
            self.Longitude,
        )
