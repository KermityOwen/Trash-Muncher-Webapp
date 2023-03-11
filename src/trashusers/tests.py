from rest_framework.test import (
    APITestCase,
    APIClient,
    force_authenticate,
)
from rest_framework import status
from .models import Player, GameKeeper, User, Team
from django.contrib.auth.models import Group


class UserViewsetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="first_user",
            email="first_user@example.com",
            first_name="first",
            last_name="user",
            password="secure_password_rock",
        )
        self.player = Player.objects.create(
            user=self.user, team=Team.objects.get_or_create(id=1, name="Red")[0]
        )
        self.client = APIClient()
        self.url = "/api"

    def test_create_player(self):
        self.client.force_authenticate()
        response = self.client.post(
            self.url + "/users/player-register/",
            {
                "user": {
                    "username": "test_user",
                    "first_name": "Test",
                    "last_name": "User",
                    "email":"test_user@example.com",
                    "password": "secure_password",
                },
                "team": {"name": "Red"},
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_gamekeeper(self):
        self.client.force_authenticate()
        response = self.client.post(
            self.url + "/users/gamekeeper-register/",
            {
                "user": {
                    "username": "test_user",
                    "first_name": "Test",
                    "last_name": "User",
                    "email":"test_user@example.com",
                    "password": "secure_password",
                }
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url + "/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], self.user.username)

    def test_retreive_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url + "/users/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["username"], self.user.username)
