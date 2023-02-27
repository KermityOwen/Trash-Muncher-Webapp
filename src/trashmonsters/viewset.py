from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 

from .models import TrashMonsters
from .serializer import TMSerializer
from trashmain.permissions import isPlayer, isGameKeeper

from geopy import distance



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTMs(request):
    TMs = TrashMonsters.objects.all()
    serializer = TMSerializer(TMs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getTM(request):
    TM_ID = request.data.get("TM_ID", None)
    TM = TrashMonsters.objects.get(TM_ID = TM_ID)
    serializer = TMSerializer(TM, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, isGameKeeper])
def addTM(request):
    serializer = TMSerializer(data=request.data)
    if (serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calcDistance(request):
    TM_ID = request.data.get("TM_ID", None)
    TM = TrashMonsters.objects.get(TM_ID = TM_ID)

    target = (TM.Latitude, TM.Longitude)
    origin = (request.data.get("o-lat", None), request.data.get("o-long", None))
    difference = distance.distance(target, origin).m

    return Response(difference)

@api_view(['POST'])
@permission_classes([IsAuthenticated, isGameKeeper])
def changeScore(request):
    TM_ID = request.data.get("TM_ID", None)
    T1Score = request.data.get("T1Score", None)
    T2Score = request.data.get("T2Score", None)
    T3Score = request.data.get("T3Score", None)

    TM = TrashMonsters.objects.get(TM_ID = TM_ID)
    TM.Team1_Score = T1Score
    TM.Team2_Score = T2Score
    TM.Team3_Score = T3Score

    TM.save()

    return Response(TMSerializer(TM, many=False).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, isPlayer])
def addScore(request):
    TM_ID = request.data.get("TM_ID", None)
    T1Score = request.data.get("T1Score", 0)
    T2Score = request.data.get("T2Score", 0)
    T3Score = request.data.get("T3Score", 0)

    TM = TrashMonsters.objects.get(TM_ID = TM_ID)
    TM.Team1_Score += T1Score
    TM.Team2_Score += T2Score
    TM.Team3_Score += T3Score

    TM.save()

    return Response(TMSerializer(TM, many=False).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, isGameKeeper])
def removeScore(request):
    TM_ID = request.data.get("TM_ID", None)
    T1Score = request.data.get("T1Score", 0)
    T2Score = request.data.get("T2Score", 0)
    T3Score = request.data.get("T3Score", 0)

    TM = TrashMonsters.objects.get(TM_ID = TM_ID)
    TM.Team1_Score -= T1Score
    TM.Team2_Score -= T2Score
    TM.Team3_Score -= T3Score

    TM.save()

    return Response(TMSerializer(TM, many=False).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getLeaderTeam(request):
    TM_ID = request.data.get("TM_ID", None)
    TM = TrashMonsters.objects.get(TM_ID = TM_ID)

    # Using bubble search for now (hard code for only 3 groups), can optimise or fix in the future. ceebs
    if (TM.Team1_Score >= TM.Team2_Score):
        if (TM.Team1_Score > TM.Team3_Score):
            return Response(1)
        else:
            return Response(3)
    elif (TM.Team2_Score > TM.Team3_Score):
        return Response (2)
