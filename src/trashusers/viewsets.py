from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import mixins, status, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import UserSerializer, UserPostSerializer, PlayerSerializer, GameKeeperSerializer, PasswordChangeSerializer
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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="me", name="me")
    def me(self, request):
        """Get the current authenticated user"""
        if Player.objects.filter(user=request.user).exists():
            self.serializer_class=PlayerSerializer
            serializer = self.get_serializer(Player.objects.get(user=request.user))
        if GameKeeper.objects.filter(user=request.user).exists():
            self.serializer_class=GameKeeperSerializer
            serializer = self.get_serializer(GameKeeperSerializer.objects.get(user=request.user))
        return Response(serializer.data)

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
            refresh = RefreshToken.for_user(user)
            print(refresh)
            return Response(
                {
                    "message": "Logged in successfully",
                    "user": UserSerializer(user).data,
                    "refresh":str(refresh),
                    "access":str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Invalid username or password!!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class PasswordChangeView(generics.UpdateAPIView):
    """
    An endpoint that allows a user to receive an email to change their password
    """
    serializer_class = PasswordChangeSerializer
    model = get_user_model()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return user

    def update(self, request):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # If the password entered is not correct, respond with 400
            if not self.object.check_password(serializer.data.get("old_pwd")):
                return Response({
                    "old_pwd": ["Wrong Password"]
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get the new password from the request and set it as the user's password
            self.object.set_password(serializer.data.get("new_pwd"))

            # Save changes to the database 
            self.object.save()

            return Response(
                {"status":"success",
                 "code":status.HTTP_200_OK,
                 "message":"Password updated successfully",
                 "data":[]
                }
            )
        
        # Returns 400 if there was an error getting the serialized info
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
