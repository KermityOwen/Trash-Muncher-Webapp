from django.test import TestCase
from .models import Images
from trashusers.models import User, GameKeeper, Team, Player
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate, APIRequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.parsers import MultiPartParser, FormParser



# Create your tests here.
class ImageSubmissionViewsetTest(APITestCase):
    factory = APIRequestFactory()
    def setUp(self):
        # Create two test users 
        self.user_one = User.objects.create(username="example_gamekeeper",
                                        first_name="test",
                                        last_name="gamekeeper",
                                        password="secure_password")

        self.user_two = User.objects.create(username="example_player",
                                        first_name="test",
                                        last_name="player",
                                        password="secure_password")
        
        
        # Make one of the users a player and the other a gamekeeper
        self.gk = GameKeeper.objects.create(user=self.user_one)

        self.player = Player.objects.create(user=self.user_two, 
                                            team=Team.objects.get_or_create
                                            (id=1, name="Red")[0])

        # Initialising the APIs
        self.client = APIClient()
        self.url = "/api"

    
    def test_submit_image(self):
        # add the API call to be tested to the URL 
        parser_classes = (MultiPartParser, FormParser)
        file = SimpleUploadedFile(name="test.jpg", 
                                            content=b"", 
                                            content_type='image/jpeg')


        # Getting a dummy response
        request = self.client.post(self.url + "/images/submit-images/", {"image":file}, format="json")
        self.client.force_authenticate(request, self.player)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)




        
        