from rest_framework.test import (
    APITestCase,
    APIClient,
)
from rest_framework import status
from trashusers.models import Player, GameKeeper, User, Team
from .models import TrashMonsters
from django.contrib.auth.models import Group
import json


class TrashmonsterViewsetTest(APITestCase):
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
        self.trashmonster_one = TrashMonsters.objects.create(Longitude=11, Latitude=2)
        self.trashmonster_two = TrashMonsters.objects.create(Longitude=1, Latitude=4)
        self.trashmonster_three = TrashMonsters.objects.create(Longitude=4, Latitude=5)

        # Initialising the APIs
        self.client = APIClient()
        self.url = "/api"

    def test_get_TMs_player(self):
        self.client.force_authenticate(self.user_player)
        response = self.client.get(self.url + '/monsters/get-tms', format='json')
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_TMs_gamekeeper(self):
        self.client.force_authenticate(self.user_gk)
        response = self.client.get(self.url + '/monsters/get-tms', format='json')
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_TM_player(self):
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/get-tm', {'TM_ID':1},format='json')
        self.assertEqual(response.data['TM_ID'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_TM_gamekeeper(self):
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(self.url + '/monsters/get-tm', {'TM_ID':1},format='json')
        self.assertEqual(response.data['TM_ID'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_TM_gamekeeper(self):
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(self.url + '/monsters/add-tm', {'Latitude':1.0, 'Longitude':1.0},format='json')
        self.assertEqual(TrashMonsters.objects.count(), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_TM_player_deny(self):
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/add-tm', {'Latitude':1.0, 'Longitude':1.0},format='json')
        self.assertEqual(TrashMonsters.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_calcDistance_player(self):
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/calculate-distance', {'TM_ID':1, 'o-lat':2.0, 'o-long':11.0},format='json')
        self.assertEqual(response.content, b'0.0')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_calcDistance_gamekeeper(self):
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(self.url + '/monsters/calculate-distance', {'TM_ID':1, 'o-lat':2.0, 'o-long':11.0},format='json')
        self.assertEqual(response.content, b'0.0')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_verifyDistance_player(self):
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/verify-distance', {'TM_ID':1, 'o-lat':2.0, 'o-long':11.0},format='json')
        self.assertEqual(response.content, b'true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_verifyDistance_gamekeeper(self):
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(self.url + '/monsters/verify-distance', {'TM_ID':1, 'o-lat':2.0, 'o-long':11.0},format='json')
        self.assertEqual(response.content, b'true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_changeScore_gamekeeper(self):
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(self.url + '/monsters/change-score', {"TM_ID":1, "T1Score":1, "T2Score":2, "T3Score":4},format='json')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content["Team1_Score"], 1)
        self.assertEqual(content["Team2_Score"], 2)
        self.assertEqual(content["Team3_Score"], 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_changeScore_player(self):
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/change-score', {"TM_ID":1, "T1Score":1, "T2Score":2, "T3Score":4},format='json')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(TrashMonsters.objects.get(TM_ID=1).Team1_Score, 0)
        self.assertEqual(TrashMonsters.objects.get(TM_ID=1).Team2_Score, 0)
        self.assertEqual(TrashMonsters.objects.get(TM_ID=1).Team3_Score, 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_addScore_gamekeeper(self):
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(self.url + '/monsters/add-score', {"TM_ID":1, "T1Score":1, "T2Score":1, "T3Score":1},format='json')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content["Team1_Score"], 1)
        self.assertEqual(content["Team2_Score"], 1)
        self.assertEqual(content["Team3_Score"], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_addScore_player(self):
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/add-score', {"TM_ID":1, "T1Score":1, "T2Score":1, "T3Score":1},format='json')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content["Team1_Score"], 1)
        self.assertEqual(content["Team2_Score"], 1)
        self.assertEqual(content["Team3_Score"], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_removeScore_gamekeeper(self):
        self.client.force_authenticate(self.user_gk)
        self.client.post(self.url + '/monsters/change-score', {"TM_ID":1, "T1Score":9, "T2Score":9, "T3Score":9},format='json')
        response = self.client.post(self.url + '/monsters/remove-score', {"TM_ID":1, "T1Score":1, "T2Score":1, "T3Score":0},format='json')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content["Team1_Score"], 8)
        self.assertEqual(content["Team2_Score"], 8)
        self.assertEqual(content["Team3_Score"], 9)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_removeScore_player(self):
        self.client.force_authenticate(self.user_gk)
        self.client.post(self.url + '/monsters/change-score', {"TM_ID":1, "T1Score":9, "T2Score":9, "T3Score":9},format='json')

        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/remove-score', {"TM_ID":1, "T1Score":1, "T2Score":1, "T3Score":0},format='json')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(TrashMonsters.objects.get(TM_ID=1).Team1_Score, 9)
        self.assertEqual(TrashMonsters.objects.get(TM_ID=1).Team2_Score, 9)
        self.assertEqual(TrashMonsters.objects.get(TM_ID=1).Team3_Score, 9)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_getLeader_player(self):
        self.client.force_authenticate(self.user_gk)
        self.client.post(self.url + '/monsters/change-score', {"TM_ID":1, "T1Score":9, "T2Score":8, "T3Score":8},format='json')
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/get-leader', {"TM_ID":1},format='json')
        self.assertEqual(response.content, b'1')

    def test_getLeader_gamekeeper(self):
        self.client.force_authenticate(self.user_gk)
        self.client.post(self.url + '/monsters/change-score', {"TM_ID":1, "T1Score":9, "T2Score":8, "T3Score":8},format='json')
        response = self.client.post(self.url + '/monsters/get-leader', {"TM_ID":1},format='json')
        self.assertEqual(response.content, b'1')