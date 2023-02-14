from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, PlayerSerializer, GamekeeperSerializer
from .models import Player

class PlayerRegistrationViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = []
    serializer_class = PlayerSerializer
    def post(self, request):
        """
        Create a student record
        :param request: Request object for creating Player/GameKeeper
        :return: Returns data of created Player/GameKeeper
        """
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

class GamekeeperRegistrationViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = []
    serializer_class = GamekeeperSerializer
    def post(self, request):
        """
        Create a student record
        :param request: Request object for creating Player/GameKeeper
        :return: Returns data of created Player/GameKeeper
        """
        serializer = GamekeeperSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


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
