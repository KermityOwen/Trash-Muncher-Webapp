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
        """
        Sets up the testing environment by creating example users
        """
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
        """
        Ensure that players can be created provided that they supply
        the correct information
        :assertions: Expecting a 201 response code is returned
        """
        self.client.force_authenticate()
        response = self.client.post(
            self.url + "/users/player-register/",
            {
                "user": {
                    "username": "test_user",
                    "first_name": "Test",
                    "last_name": "User",
                    "email": "test_user@example.com",
                    "password": "secure_password",
                },
                "team": {"name": "Red"},
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_gamekeeper(self):
        """
        Ensure that gamekeepers can be created provided that they supply
        the correct information
        :assertions: Expecting a 201 response code is returned
        """
        self.client.force_authenticate()
        response = self.client.post(
            self.url + "/users/gamekeeper-register/",
            {
                "user": {
                    "username": "test_user",
                    "first_name": "Test",
                    "last_name": "User",
                    "email": "test_user@example.com",
                    "password": "secure_password",
                }
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user(self):
        """
        Ensure that information about a user can be obtained
        :assertions: Expecting a 200 response code is returned
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url + "/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], self.user.username)

    def test_retreive_user(self):
        """
        Ensure that information about a user can be obtained based on their id
        :assertions: Expecting a 200 response code is returned
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url + "/users/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["username"], self.user.username)

    def test_login(self):
        user = User.objects.create(
            username="test_login",
            email="test_login@example.com",
            first_name="test",
            last_name="login",
        )
        user.set_password("secure_password_rock")
        user.save()
        response = self.client.post(
            self.url + "/users/login/",
            {"username": "test_login", "password": "secure_password_rock"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
