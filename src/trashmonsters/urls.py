from django.urls import path
from . import viewset

urlpatterns = [
    path('get', viewset.getTM),
    path('add', viewset.addTM)
]
