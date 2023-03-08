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
        # Create two test users (one gamekeeper, one user)
        self.user_gk = User.objects.create(username="example_gamekeeper",
                                        first_name="test",
                                        last_name="gamekeeper",
                                        password="secure_password")
        
        self.gk = GameKeeper.objects.create(user=self.user_gk)

        self.user_player = User.objects.create(username="example_player",
                                        first_name="test",
                                        last_name="player",
                                        password="secure_password")

        self.player = Player.objects.create(user=self.user_player, 
                                            team=Team.objects.get_or_create
                                            (id=1, name="Red")[0])

        # Create three test trashmonsters                                    
        self.trashmonster_one = TrashMonsters.objects.create(Longitude=11, Latitude=2)
        self.trashmonster_two = TrashMonsters.objects.create(Longitude=1, Latitude=4)
        self.trashmonster_three = TrashMonsters.objects.create(Longitude=4, Latitude=5)

        # Initialising the APIs
        self.client = APIClient()
        self.url = "/api"

    def test_get_TMs_player(self):
        """
        Test to ensure that gamekeepers can access the endpoint and get info about a single trashmonster 
        :assertions: Expecting a 200 response code is returned
                     Expecting three trashmonsters to be in the response 
        """
        self.client.force_authenticate(self.user_player)
        response = self.client.get(self.url + '/monsters/get-tms', format='json')
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_TMs_gamekeeper(self):
        """
        Test to ensure that gamekeepers can access the endpoint and get info about a single trashmonster 
        :assertions: Expecting a 200 response code is returned
                     Expecting three trashmonsters to be in the response 
        """
        self.client.force_authenticate(self.user_gk)
        response = self.client.get(self.url + '/monsters/get-tms', format='json')
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_TM_player(self):
        """
        Test to ensure that gamekeepers can access the endpoint and get info about a single trashmonster 
        :assertions: Expecting a 200 response code is returned
                     Expecting a trashmonster with ID 1 to be in the response
        """
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/get-tm', {'TM_ID':1},format='json')
        self.assertEqual(response.data['TM_ID'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_TM_gamekeeper(self):
        """
        Test to ensure that gamekeepers can access the endpoint and get info about a single trashmonster 
        :assertions: Expecting a 200 response code is returned
                     Expecting a trashmonster with ID 1 to be in the response
        """
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(self.url + '/monsters/get-tm', {'TM_ID':1},format='json')
        self.assertEqual(response.data['TM_ID'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_TM_gamekeeper(self):
        """
        Test to ensure that gamekeepers can access the endpoint and can create a trashmonster
        :assertions: Expecting a 200 response code is returned
                     Expecting the number of trashmonsters to be 4 (new trashmonster created)
        """
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(self.url + '/monsters/add-tm', {'Latitude':1.0, 'Longitude':1.0},format='json')
        self.assertEqual(TrashMonsters.objects.count(), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_TM_player_deny(self):
        """
        Test to ensure that gamekeepers can access the endpoint and can create a trashmonster
        :assertions: Expecting a 200 response code is returned
                     Expecting the number of trashmonsters to be 3 (no new trashmonster)
        """
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/add-tm', {'Latitude':1.0, 'Longitude':1.0},format='json')
        self.assertEqual(TrashMonsters.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_calcDistance_player(self):
        """
        Test to ensure that players can access the endpoint and calculate their distance to a trashmonster
        :assertions: Expecting a 200 response code is returned
                     Expecting that the distance between the player and the trashmonster is zero
        """
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/calculate-distance', {'TM_ID':1, 'o-lat':2.0, 'o-long':11.0},format='json')
        self.assertEqual(response.content, b'0.0')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_calcDistance_gamekeeper(self):
        """
        Test to ensure that players can access the endpoint and calculate their distance to a trashmonster
        :assertions: Expecting a 200 response code is returned
                     Expecting that the distance between the player and the trashmonster is zero
        """
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(self.url + '/monsters/calculate-distance', {'TM_ID':1, 'o-lat':2.0, 'o-long':11.0},format='json')
        self.assertEqual(response.content, b'0.0')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_verifyDistance_player(self):
        """
        Test to ensure that players can access the endpoint and verify that were within a valid distance 
        from the trashmonster 
        :assertions: Expecting a 200 response code is returned
                     Expecting that the distance is valid (true)
        """
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/verify-distance', {'TM_ID':1, 'o-lat':2.0, 'o-long':11.0},format='json')
        self.assertEqual(response.content, b'true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_verifyDistance_gamekeeper(self):
        """
        Test to ensure that gamekeepers can access the endpoint and verify that were within a valid distance 
        from the trashmonster 
        :assertions: Expecting a 200 response code is returned
                     Expecting that the distance is valid (true)
        """
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(self.url + '/monsters/verify-distance', {'TM_ID':1, 'o-lat':2.0, 'o-long':11.0},format='json')
        self.assertEqual(response.content, b'true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_changeScore_gamekeeper(self):
        """
        Test to ensure that gamekeepers can access the endpoint and change trashmonster scores  
        :assertions: Expecting a 200 response code is returned
                     Expecting that the score for all three trashmonsters has been changed
        """
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(self.url + '/monsters/change-score', {"TM_ID":1, "T1Score":1, "T2Score":2, "T3Score":4},format='json')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content["Team1_Score"], 1)
        self.assertEqual(content["Team2_Score"], 2)
        self.assertEqual(content["Team3_Score"], 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_changeScore_player(self):
        """
        Test to ensure that players cannot access the endpoint 
        :assertions: Expecting a 403 response code is returned
                     Expecting that the score for all three trashmonsters has not been changed
        """
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/change-score', {"TM_ID":1, "T1Score":1, "T2Score":2, "T3Score":4},format='json')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(TrashMonsters.objects.get(TM_ID=1).Team1_Score, 0)
        self.assertEqual(TrashMonsters.objects.get(TM_ID=1).Team2_Score, 0)
        self.assertEqual(TrashMonsters.objects.get(TM_ID=1).Team3_Score, 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_addScore_gamekeeper(self):
        """
        Test to ensure that Test to ensure that players can access the endpoint and add scores to trashmonsters 
        of their choice  
        :assertions: Expecting a 200 response code is returned
                     Expecting that the score for all three trashmonsters has been incremented by 1
        """
        self.client.force_authenticate(self.user_gk)
        response = self.client.post(self.url + '/monsters/add-score', {"TM_ID":1, "T1Score":1, "T2Score":1, "T3Score":1},format='json')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content["Team1_Score"], 1)
        self.assertEqual(content["Team2_Score"], 1)
        self.assertEqual(content["Team3_Score"], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_addScore_player(self):
        """
        Test to ensure that players can access the endpoint and add scores to trashmunchers of their choice  
        :assertions: Expecting a 200 response code is returned
                     Expecting that the score for all three trashmonsters has been incremented by 1
        """
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/add-score', {"TM_ID":1, "T1Score":1, "T2Score":1, "T3Score":1},format='json')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content["Team1_Score"], 1)
        self.assertEqual(content["Team2_Score"], 1)
        self.assertEqual(content["Team3_Score"], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_removeScore_gamekeeper(self):
        """
        Test to ensure that gaemkeepers can access the endpoint and remove scores from certain trashmonsters 
        :assertions: Expecting a 200 response code is returned
                     Expecting that the scores for two trashmonsters has decreased and the other isn't affected 
        """
        self.client.force_authenticate(self.user_gk)
        self.client.post(self.url + '/monsters/change-score', {"TM_ID":1, "T1Score":9, "T2Score":9, "T3Score":9},format='json')
        response = self.client.post(self.url + '/monsters/remove-score', {"TM_ID":1, "T1Score":1, "T2Score":1, "T3Score":0},format='json')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content["Team1_Score"], 8)
        self.assertEqual(content["Team2_Score"], 8)
        self.assertEqual(content["Team3_Score"], 9)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_removeScore_player(self):
        """
        Test to ensure that players cannot access the endpoint 
        :assertions: Expecting a 403 response code is returned
                     Expecting that the scores for all the trashmonsters haven't been changed 
        """
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
        """
        Test to ensure that players can access the endpoint and view each monster's leading team
        by having the gamekeeper change a score for one monster 
        :assertions: Expecting that leading team from the request is team 1
        """
        self.client.force_authenticate(self.user_gk)
        self.client.post(self.url + '/monsters/change-score', {"TM_ID":1, "T1Score":9, "T2Score":8, "T3Score":8},format='json')
        self.client.force_authenticate(self.user_player)
        response = self.client.post(self.url + '/monsters/get-leader', {"TM_ID":1},format='json')
        self.assertEqual(response.content, b'1')

    def test_getLeader_gamekeeper(self):
        """
        Test to ensure that players can access the endpoint and view each monster's leading team
        by having the gamekeeper change a score for one monster 
        :assertions: Expecting that leading team from the request is team 1
        """
        self.client.force_authenticate(self.user_gk)
        self.client.post(self.url + '/monsters/change-score', {"TM_ID":1, "T1Score":9, "T2Score":8, "T3Score":8},format='json')
        response = self.client.post(self.url + '/monsters/get-leader', {"TM_ID":1},format='json')
        self.assertEqual(response.content, b'1')