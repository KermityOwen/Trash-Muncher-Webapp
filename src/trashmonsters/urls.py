from django.urls import path
from . import viewset

urlpatterns = [
    path('get-tms', viewset.getTMs),
    path('get-tm', viewset.getTM),
    path('add-tm', viewset.addTM),

    path('calculate-distance', viewset.calcDistance),

    path('change-score', viewset.changeScore),
    path('add-score', viewset.addScore),
    path('remove-score', viewset.removeScore)
]

