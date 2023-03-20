from django.urls import path
from . import viewset

# List of URLs to allow for access to the endpoints
urlpatterns = [
    path("get-tms", viewset.getTMs),
    path("get-tm", viewset.getTM),
    path("add-tm", viewset.addTM),
    path("calculate-distance", viewset.calcDistance),
    path("verify-distance", viewset.verifyDistance),
    path("change-score", viewset.changeScore),
    path("add-score", viewset.addScore),
    path("remove-score", viewset.removeScore),
    path("get-leader", viewset.getLeaderTeam),
]
