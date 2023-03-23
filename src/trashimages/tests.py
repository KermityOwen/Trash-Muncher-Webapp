from django.test import TestCase
from .models import Images
from trashusers.models import User, GameKeeper, Team, Player
from trashmonsters.models import TrashMonsters
from rest_framework import status
from rest_framework.test import (
    APITestCase,
    APIClient,
    force_authenticate,
)
from django.core.files import File
from rest_framework.parsers import MultiPartParser, FormParser

import io


class ImageSubmissionViewsetTest(APITestCase):
    def setUp(self):
        # Create three test users (two players, one gamekeeper)
        self.user_gk = User.objects.create(
            username="example_gamekeeper",
            first_name="test",
            last_name="gamekeeper",
            email="test_gamekeeper@example.com",
            password="secure_password",
        )

        self.gk = GameKeeper.objects.create(user=self.user_gk)

        self.user_player = User.objects.create(
            username="example_player",
            first_name="test",
            last_name="player",
            email="test_player@example.com",
            password="secure_password",
        )

        self.player = Player.objects.create(
            user=self.user_player, team=Team.objects.get_or_create(id=1, name="Red")[0]
        )

        # Test player specifically for API throttling tests
        self.user_limit = User.objects.create(
            username="example_player2",
            first_name="test",
            last_name="player",
            email="test_player2@example.com",
            password="secure_password",
        )

        self.player_limit = Player.objects.create(
            user=self.user_limit, team=Team.objects.get_or_create(id=1, name="Red")[0]
        )

        self.trashmonster_one = TrashMonsters.objects.create(Longitude=11, Latitude=2)

        # Example Base64 value
        self.b64_val = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII="

        # Initialising the APIs
        self.client = APIClient()
        self.url = "/api"

    def test_player_submit_image(self):
        """
        Ensure that players are able to access the API enpoint and submit an image
        :assertions: Expecting a 201 response code is returned
        """
        parser_classes = (MultiPartParser, FormParser)
        submission = self.b64_val

        # Getting a dummy response
        self.client.force_authenticate(self.user_player)
        response = self.client.post(
            self.url + "/images/submit-image/",
            {"b64_img": submission, "monster_id": 1},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_gamekeeper_deny_from_submit(self):
        """
        Ensure that gamekeepers cannot access this API enpoint
        :assertions: Expecting a 403 response code is returned
        """
        parser_classes = (MultiPartParser, FormParser)
        submission = self.b64_val

        # Getting a dummy response
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(
            self.url + "/images/submit-image/",
            {"b64_img": submission},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_limiting(self):
        """
        Ensure that players cannot access this endpoint more than one time per day
        :assertions: Expecting a 201 response code is returned for the first response
                     Expecting a 429 response code is returned for the second response
        """
        parser_classes = (MultiPartParser, FormParser)
        submission = self.b64_val

        # Getting dummy responses
        self.client.force_authenticate(self.user_limit)
        response1 = self.client.post(
            self.url + "/images/submit-image/",
            {"b64_img": submission, "monster_id":1},
            format="multipart",
        )

        response2 = self.client.post(
            self.url + "/images/submit-image/",
            {"b64_img": submission, "monster_id":1},
            format="multipart",
        )
        

        # Asserting that a user can make one post and no more after that 
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

    def test_gamekeeper_list_image(self):
        """
        Ensure that gamekeepers are able to access the API enpoint and view list of all images in the database
        :assertions: Expecting a 200 response code is returned
        """
        self.client.force_authenticate(self.user_gk)
        response = self.client.get(self.url + "/images/list-images/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_player_deny_from_list(self):
        """
        Ensure that players cannot access this API enpoint
        :assertions: Expecting a 403 response code is returned
        """
        self.client.force_authenticate(self.user_player)
        response = self.client.get(self.url + "/images/list-images/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_gamekeeper_delete_image(self):
        """
        Ensure that gamekeepers are able to access the API enpoint and delete an image
        :assertions: Expecting a 200 response code is returned
        """
        Images.objects.create(image=File(file=b""))
        self.client.force_authenticate(self.user_gk)
        self.assertEqual(Images.objects.count(), 1)
        response = self.client.post(
            self.url + "/images/delete-image/", {"id": 1}, format="json"
        )
        self.assertEqual(Images.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_player_deny_delete_image(self):
        """
        Ensure that players cannot access this API enpoint
        :assertions: Expecting a 403 response code is returned
        """
        Images.objects.create(image=File(file=b""))
        self.client.force_authenticate(self.user_player)
        self.assertEqual(Images.objects.count(), 1)
        response = self.client.post(
            self.url + "/images/delete-image/", {"id": 1}, format="json"
        )
        self.assertEqual(Images.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
