from django.test import TestCase
from .models import Images
from trashusers.models import User, GameKeeper, Team, Player
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate, APIRequestFactory
from django.core.files import File
from rest_framework.parsers import MultiPartParser, FormParser

import io

from PIL import Image



# Create your tests here.
class ImageSubmissionViewsetTest(APITestCase):
    def setUp(self):
        # Create two test users 
        self.user_gk = User.objects.create(username="example_gamekeeper",
                                        first_name="test",
                                        last_name="gamekeeper",
                                        password="secure_password")
        
        self.gk = GameKeeper.objects.create(user=self.user_gk)

        self.user_player = User.objects.create(username="example_player",
                                        first_name="test",
                                        last_name="player",
                                        password="secure_password")
        
        
        # Make one of the users a player and the other a gamekeeper

        self.player = Player.objects.create(user=self.user_player, 
                                            team=Team.objects.get_or_create
                                            (id=1, name="Red")[0])

        # Initialising the APIs
        self.client = APIClient()
        self.url = "/api"
    
    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file


    
    def test_player_submit_image(self):
        # add the API call to be tested to the URL 
        parser_classes = (MultiPartParser, FormParser)
        submission = self.generate_photo_file()

        # Getting a dummy response
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + "/images/submit-image/", {"image":submission}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_gamekeeper_deny_from_submit(self):
        parser_classes = (MultiPartParser, FormParser)
        submission = self.generate_photo_file()

        # Getting a dummy response
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(self.url + "/images/submit-image/", {"image":submission}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_gamekeeper_list_image(self):
        self.client.force_authenticate(self.user_gk)
        response = self.client.get(self.url + "/images/list-images/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_player_deny_from_list(self):
        self.client.force_authenticate(self.user_player)
        response = self.client.get(self.url + "/images/list-images/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_gamekeeper_delete_image(self):
        Images.objects.create(image=File(file=b""))
        self.client.force_authenticate(self.user_gk)
        self.assertEqual(Images.objects.count(), 1)
        response = self.client.post(self.url + "/images/delete-image/", {"id":1}, format="json")
        self.assertEqual(Images.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_player_deny_delete_image(self):
        Images.objects.create(image=File(file=b""))
        self.client.force_authenticate(self.user_player)
        self.assertEqual(Images.objects.count(), 1)
        response = self.client.post(self.url + "/images/delete-image/", {"id":1}, format="json")
        self.assertEqual(Images.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        
        