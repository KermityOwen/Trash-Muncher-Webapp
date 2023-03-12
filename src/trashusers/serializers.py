from django.contrib.auth import get_user_model
from .models import Player, GameKeeper, Team
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from trashmain.auxillary import get_player_team
from trashmain.permissions import isGameKeeper, isPlayer


class UserSerializer(serializers.ModelSerializer):
    """ 
    Class that specifies which model the fields will be coming from and the fields extracted
    """
    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name", "email", "username", "is_gamekeeper"]
        read_only_fields = [
            "id",
        ]


class UserPostSerializer(serializers.ModelSerializer):
    """ 
    Class that specifies which model the fields will be coming from and the fields extracted
    """
    class Meta:
        model = get_user_model()
        read_only_fields = ["id"]
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_gamekeeper",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    """
    Function used to create a user and guarantee that the password is strong. Inherited from rest_framework

    Parameters:
    validated_data (str) - Gets the password from the serialized JSON

    Returns:
    user (user) - The new user created with the data inputted on the website 
    """
    def create(self, validated_data):
        raw_password = validated_data.pop("password")
        try:
            validate_password(raw_password)
        except ValidationError:
            raise DRFValidationError

        user = get_user_model().objects.create_user(
            password=raw_password, **validated_data
        )

        return user


class TeamSerializer(serializers.ModelSerializer):
    """ 
    Class that specifies which model the fields will be coming from and the fields extracted
    """
    class Meta:
        model = Team
        fields = ["name"]


class PlayerSerializer(serializers.ModelSerializer):
    # Need to create the teams first, before using this, could look into the idea of some kinda database initialization,
    # or simply adding it to the readme, this way is better, because you can change names of teams then if you want to set it up
    user = UserPostSerializer(required=True)
    team = TeamSerializer(required=True)

    """ 
    Class that specifies which model the fields will be coming from and the fields extracted
    """
    class Meta:
        model = Player
        fields = [
            "user",
            "team",
        ]

    """
    Function used to create a player and guarantees that the information inputted is valid. Inherited from rest_framework

    Parameters:
    validated_data (str) - Gets the user's information from the request  

    Returns:
    player (player) - The new player created from the user's data  
    """
    def create(self, validated_data):
        validated_data["is_player"] = True
        user_data = validated_data.get("user")
        user_serializer = UserPostSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.create(validated_data=user_data)
        # Overriding create function necessitates this, can be changed to take ints if preferred.
        team_data = validated_data.get("team")
        player, created = Player.objects.update_or_create(
            user=user, team=Team.objects.get(name=team_data["name"])
        )
        return player


class GameKeeperSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(required=True)

    """ 
    Class that specifies which model the fields will be coming from and the fields extracted
    """
    class Meta:
        model = GameKeeper
        fields = [
            "user",
        ]

    """
    Function used to create a gamekeeper and guarantees that the information inputted is valid. Inherited from rest_framework

    Parameters:
    validated_data (str) - Gets the user's information from the request  

    Returns:
    gamekeeper (gamekeeper) - The new gamekeeper created from the user's data  
    """
    def create(self, validated_data):
        validated_data["is_gamekeeper"] = True
        user_data = validated_data.get("user")
        user_serializer = UserPostSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=ValueError):
            user = user_serializer.create(validated_data=user_data)
        else:
            print(user_data)
        gamekeeper, created = GameKeeper.objects.update_or_create(user=user)
        return gamekeeper

"""
Class to serialize and get the old password from the database and the new one
from the request
"""
class PasswordChangeSerializer(serializers.Serializer):
    model = get_user_model()
    old_pwd = serializers.CharField(required=True)
    new_pwd = serializers.CharField(required=True)
