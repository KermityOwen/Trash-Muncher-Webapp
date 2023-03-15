from rest_framework.routers import SimpleRouter
from django.urls import path, include
from . import viewsets
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "TrashMunchers Users"

# Create a SimpleRouter to allow for the Viewsets to be registered as endpoints
users_router = SimpleRouter()
users_router.register(
    r"player-register", viewsets.PlayerRegistrationViewset, basename="users"
)
users_router.register(
    r"gamekeeper-register", viewsets.GamekeeperRegistrationViewset, basename="users"
)
users_router.register(r"", viewsets.UserViewSet, basename="")

# List of URLs that link to their respective viewset endpoints 
urlpatterns = [
    path("login/", viewsets.LoginView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", viewsets.LogoutView.as_view()),
    path(
        "change-password/",
        viewsets.PasswordChangeView.as_view(),
        name="change-password",
    ),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password-reset')),
]
urlpatterns += users_router.urls
