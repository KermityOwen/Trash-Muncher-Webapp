from rest_framework.routers import SimpleRouter
from django.urls import path
from . import viewsets

app_name = "TrashMunchers Users"

users_router = SimpleRouter()
users_router.register(r"player-register", viewsets.PlayerRegistrationViewset, basename="users")
users_router.register(r"gamekeeper-register", viewsets.GamekeeperRegistrationViewset, basename="users")
users_router.register(r"user-register", viewsets.UserRegistrationViewset, basename="users")
urlpatterns = [
    path('login/', viewsets.LoginView.as_view()),
]
urlpatterns += users_router.urls