from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import TrashMonsters
from .serializer import TMSerializer
from trashmain.permissions import isPlayer, isGameKeeper
from rest_framework import status

from geopy import distance
from random import randint
import json, os

cached_leader = {}


"""
Function to reset the database used for testing by checking that there are 
TrashMonsters in the database and create three TrashMonster objects 
"""
def restart_testing_db():
    TMs = TrashMonsters.objects.all()
    if len(TMs) == 0:
        TrashMonsters.objects.create(Longitude=11, Latitude=2)
        TrashMonsters.objects.create(Longitude=1, Latitude=4)
        TrashMonsters.objects.create(Longitude=4, Latitude=5)
    for TM in TMs:
        TM.Team1_Score = randint(1, 99)
        TM.Team2_Score = randint(1, 99)
        TM.Team3_Score = randint(1, 99)
        TM.save()


"""
Function to carry out a bubble search to find which team has the highest monster 

Parameters:
TM (TrashMonster) - The TrashMonster that we are trying to find the leader for 

Returns:
1 (int) - Team 1 is the leading team for this monster 
2 (int) - Team 2 is the leading team for this monster 
3 (int) - Team 3 is the leading team for this monster 
"""
def bubble_search(TM: TrashMonsters):
    if TM.Team1_Score >= TM.Team2_Score:
        if TM.Team1_Score > TM.Team3_Score:
            return 1
        else:
            return 3
    elif TM.Team2_Score > TM.Team3_Score:
        return 2
    else:
        return 3


"""
Function to find out who the current leader is so that it's always displayed to the user. 
Finds the leader of which team currently has the lead for each team 
"""
def calculate_cached_leader():
    try:
        TMs = TrashMonsters.objects.all()
        for TM in TMs:
            # print (bubble_search(TM))
            cached_leader[TM.TM_ID] = bubble_search(TM)
        print(cached_leader)
    except:
        print("DB not yet set up. Run migrate before trying again.")


"""
Function to find out who the current leader is so that it's always displayed to the user. 
Finds the leader of which team currently has the lead for each team.
"""
def calculate_specific_leader(TM_ID):
    TM = TrashMonsters.objects.get(TM_ID=TM_ID)
    cached_leader[TM.TM_ID] = bubble_search(TM)



"""
For information regarding the API views, please view readme.md and read the API documentation 
"""
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTMs(request):
    TMs = TrashMonsters.objects.all()
    serializer = TMSerializer(TMs, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def getTM(request):
    TM_ID = request.data.get("TM_ID", None)
    TM = TrashMonsters.objects.get(TM_ID=TM_ID)
    serializer = TMSerializer(TM, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, isGameKeeper])
def addTM(request):
    serializer = TMSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def calcDistance(request):
    TM_ID = request.data.get("TM_ID", None)
    TM = TrashMonsters.objects.get(TM_ID=TM_ID)

    target = (TM.Latitude, TM.Longitude)
    origin = (request.data.get("o-lat", None), request.data.get("o-long", None))
    difference = distance.distance(target, origin).m

    return Response(difference)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verifyDistance(request):
    TM_ID = request.data.get("TM_ID", None)
    TM = TrashMonsters.objects.get(TM_ID=TM_ID)

    target = (TM.Latitude, TM.Longitude)
    origin = (request.data.get("o-lat", None), request.data.get("o-long", None))
    difference = distance.distance(target, origin).m

    # Value can be changed if you would like to increase the leeway a user receives 
    if difference <= 50:
        return Response(True)
    else:
        return Response(False)


@api_view(["POST"])
@permission_classes([IsAuthenticated, isGameKeeper])
def changeScore(request):
    TM_ID = request.data.get("TM_ID", None)
    TM = TrashMonsters.objects.get(TM_ID=TM_ID)
    T1Score = request.data.get("T1Score", TM.Team1_Score)
    T2Score = request.data.get("T2Score", TM.Team2_Score)
    T3Score = request.data.get("T3Score", TM.Team3_Score)

    TM.Team1_Score = T1Score
    TM.Team2_Score = T2Score
    TM.Team3_Score = T3Score

    TM.save()
    calculate_specific_leader(TM_ID)

    return Response(TMSerializer(TM, many=False).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addScore(request):
    TM_ID = request.data.get("TM_ID", None)
    T1Score = request.data.get("T1Score", 0)
    T2Score = request.data.get("T2Score", 0)
    T3Score = request.data.get("T3Score", 0)

    TM = TrashMonsters.objects.get(TM_ID=TM_ID)
    TM.Team1_Score += T1Score
    TM.Team2_Score += T2Score
    TM.Team3_Score += T3Score

    TM.save()
    calculate_specific_leader(TM_ID)

    return Response(TMSerializer(TM, many=False).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, isGameKeeper])
def removeScore(request):
    TM_ID = request.data.get("TM_ID", None)
    T1Score = request.data.get("T1Score", 0)
    T2Score = request.data.get("T2Score", 0)
    T3Score = request.data.get("T3Score", 0)

    TM = TrashMonsters.objects.get(TM_ID=TM_ID)
    TM.Team1_Score -= T1Score
    TM.Team2_Score -= T2Score
    TM.Team3_Score -= T3Score

    TM.save()
    calculate_specific_leader(TM_ID)

    return Response(TMSerializer(TM, many=False).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def getLeaderTeam(request):
    TM_ID = request.data.get("TM_ID", None)
    TM = TrashMonsters.objects.get(TM_ID=TM_ID)

    # Using bubble search for now (hard code for only 3 groups), can optimise or fix in the future. ceebs
    if TM.Team1_Score >= TM.Team2_Score:
        if TM.Team1_Score > TM.Team3_Score:
            return Response(1)
        else:
            return Response(3)
    elif TM.Team2_Score > TM.Team3_Score:
        return Response(2)
    else:
        return Response(3)
