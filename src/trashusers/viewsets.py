from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, UserPostSerializer, PlayerSerializer, GameKeeperSerializer
from .models import Player, GameKeeper, User


class PlayerRegistrationViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Player.objects.all()
    authentication_classes = []
    serializer_class = PlayerSerializer
    

class GamekeeperRegistrationViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = GameKeeper.objects.all()
    authentication_classes = []
    serializer_class = GameKeeperSerializer

class UserRegistrationViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    authentication_classes = []
    serializer_class = UserPostSerializer


class LoginView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, format=None):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        if username is None or password is None:
            return Response(
                {"message": "Username and password cannot be empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # CsrfViewMiddleware automatically adds csrf token as cookie
            # SessionMiddleware automatically adds session id as cookie
            return Response(
                {
                    "message": "Logged in successfully",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Invalid username or password!!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponse("Logged out", status=status.HTTP_200_OK)
