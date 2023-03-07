from rest_framework.test import (
    APITestCase,
    APIClient,
)
from rest_framework import status
from trashusers.models import Player, GameKeeper, User, Team
from .models import TrashMonsters
from django.contrib.auth.models import Group


class TrashmonsterViewsetTest(APITestCase):
    def setUp(self):
        self.user_one = User.objects.create(username="example_player",
                                        first_name="test",
                                        last_name="player",
                                        password="secure_password")

        self.player = Player.objects.create(user=self.user_one, 
                                            team=Team.objects.get_or_create
                                            (id=1, name="Red")[0])

        self.user_two = User.objects.create(username="example_gamekeeper",
                                        first_name="test",
                                        last_name="gamekeeper",
                                        password="secure_password")

        self.gamekeeper = GameKeeper.objects.create(user=self.user_two)

        TrashMonsters.objects.create(Longitude=11, Latitude=2)
        TrashMonsters.objects.create(Longitude=1, Latitude=4)
        TrashMonsters.objects.create(Longitude=4, Latitude=5)

        self.client = APIClient()
        self.url = "http://google.com/fuckoff"

    def test_get_TMs(self):
        response = self.client.get(self.url)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
