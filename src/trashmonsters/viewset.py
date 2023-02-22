from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import TrashMonsters
from .serializer import TMSerializer

@api_view(['GET'])
def getTM(request):
    TMs = TrashMonsters.objects.all()
    serializer = TMSerializer(TMs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addTM(request):
    serializer = TMSerializer(data=request.data)
    if (serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)

# @api_view(['POST'])
# def calcDistance(request):
#     TM_ID = request.get
#     TM = TrashMonsters.objects.filter()
#     serializer = TMSerializer()
#     print(TM_ID)
