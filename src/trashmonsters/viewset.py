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


def calculate_cached_leader():
    try:
        TMs = TrashMonsters.objects.all()
        for TM in TMs:
            # print (bubble_search(TM))
            cached_leader[TM.TM_ID] = bubble_search(TM)
        print(cached_leader)
    except:
        print("DB not yet set up. Run migrate before trying again.")


def calculate_specific_leader(TM_ID):
    TM = TrashMonsters.objects.get(TM_ID=TM_ID)
    cached_leader[TM.TM_ID] = bubble_search(TM)


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
