from rest_framework.test import (
    APITestCase,
    APIClient,
)
from rest_framework import status
from .models import User
from django.contrib.auth.models import Group


class UserViewsetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="first_user", first_name="first", last_name="user",password="first_password"
        )
        self.client = APIClient()
        self.url = "/api"

    def test_create_user(self):
        self.client.force_authenticate()
        response = self.client.post(
            self.url + "/player-register/",
            {
                "username": "test_user",
                "first_name": "Test",
                "last_name": "User",
                "password": "secure_password",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url + "/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)

    def test_retreive_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url + "/users/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["username"], self.user.username)

    def test_login(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "username": self.user.username,
                "password": self.user.password,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
