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


from .serializers import (
    UserSerializer,
    UserPostSerializer,
    PlayerSerializer,
    GameKeeperSerializer,
    PasswordChangeSerializer,
)
from .models import Player, GameKeeper, User, GkEmail


class PlayerRegistrationViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Player.objects.all()
    authentication_classes = []
    serializer_class = PlayerSerializer


class GamekeeperRegistrationViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = GameKeeper.objects.all()
    authentication_classes = []
    serializer_class = GameKeeperSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Checking if the email submitted is in the table of allowed emaisl maintained by the superuser
        print(serializer.validated_data)
        valid_email = GkEmail.objects.filter(valid_email=serializer.validated_data['user']['email']).exists()
        print(valid_email)
        if not valid_email:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        """
        Gets the current authenticated user. Checks whether their data can be found in either
        the Player database or the Gamkeeper database

        Returns:
        Response(serializer.data) - Data from the serializer 
        """

        # Get the current authenticated user
        if Player.objects.filter(user=request.user).exists():
            self.serializer_class = PlayerSerializer
            serializer = self.get_serializer(Player.objects.get(user=request.user))
        if GameKeeper.objects.filter(user=request.user).exists():
            self.serializer_class = GameKeeperSerializer
            serializer = self.get_serializer(GameKeeper.objects.get(user=request.user))
        return Response(serializer.data)



class LoginView(APIView):
    """
    Creates an endpoint to allow users to login 
    """
    permission_classes = ()
    authentication_classes = ()

    
    def post(self, request, format=None):
        """
        Provides the endpoint with post functionality. Allows users to send a post 
        request to login 

        Returns:
        Response(status.code) - Either responds with a 400 code if they have left input fields blank
                                or responds with a 200 code if they have successfully logged in 
        """
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
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Invalid username or password!!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    """
    Creates an endpoint to allow users to logout 
    """
    permission_classes = (IsAuthenticated,)

    
    def post(self, request):
        """
        Provides the endpoint with post functionality. Allows users to send a post 
        request to logout

        Returns:
        Response(status.code) - Either responds with a 205 or 400 response code based on the outcome 
                                of attempting to logout 
        """
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(generics.UpdateAPIView):
    """
    Creates an endpoint to allow users to change their password 
    """
    serializer_class = PasswordChangeSerializer
    model = get_user_model()
    permission_classes = [IsAuthenticated]

    
    def get_object(self):
        """
        Gets the current user making the request 

        Returns:
        user (user) - The current user making the request 
        """
        user = self.request.user
        return user

    
    def update(self, request):
        """
        Ensures that the user entered the correct password to allow them to change it 

        Returns:
        Response(information) (response) - Informs the user whether they have entered the correct password. 
        Produces a 400 BAD request if the user entered the wrong password for their old password 
        """
        
        # Get the current user 
        self.object = self.get_object()
        # Serialize the data submitted 
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # If the password entered is not correct, respond with 400
            if not self.object.check_password(serializer.data.get("old_pwd")):
                return Response(
                    {"old_pwd": ["Wrong Password"]}, status=status.HTTP_400_BAD_REQUEST
                )

            # Get the new password from the request and set it as the user's password
            self.object.set_password(serializer.data.get("new_pwd"))

            # Save changes to the database
            self.object.save()

            # Inform the user that their password has successfully been changed 
            return Response(
                {
                    "status": "success",
                    "code": status.HTTP_200_OK,
                    "message": "Password updated successfully",
                    "data": [],
                }
            )

        # Returns 400 if there was an error getting the serialized info
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
