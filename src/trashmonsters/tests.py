from rest_framework.test import (
    APITestCase,
    APIClient,
)
from rest_framework import status
from trashusers.models import Player, GameKeeper, User, Team
from django.contrib.auth.models import Group


class TrashmonsterViewsetTest(APITestCase):
    def setUp(self):
        self.user_one = User.objects.create(username="first_user", first_name="first", last_name="user",password="secure_password_rock")
        self.player = Player.objects.create(
            user=self.user_one, team=Team.objects.get_or_create(id=1, name='Red')[0]
        )
        self.user_two = User.objects.create(username="second_user", first_name="second", last_name="user",password="secure_password_rock")
        self.gamekeeper = GameKeeper.objects.create(
            user=self.user_two
        )
        self.client = APIClient()
        self.url = "/api"
