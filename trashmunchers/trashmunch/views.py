from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

"""
Example view that displays Hello World
"""
def getRoutes(request):
    return JsonResponse('Hello World', safe=False)