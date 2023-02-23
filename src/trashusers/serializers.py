from django.contrib.auth import get_user_model
from .models import Player, GameKeeper, Team
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from trashmain.auxillary import get_player_team
from trashmain.permissions import isGameKeeper, isPlayer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
        ]
        read_only_fields = [
            "id",
        ]

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        read_only_fields = ["id"]
        fields = ["username", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

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
    class Meta:
        model = Team
        fields = ["name"]

class PlayerSerializer(serializers.ModelSerializer):
    # Need to create the teams first, before using this, could look into the idea of some kinda database initialization, 
    # or simply adding it to the readme, this way is better, because you can change names of teams then if you want to set it up
    user = UserPostSerializer(required=True)
    team = TeamSerializer(required=True)

    class Meta:
        model = Player
        fields = [
            "user",
            "team",
        ]
    def create(self, validated_data):
        user_data = validated_data.get('user')
        user_serializer = UserPostSerializer(data=user_data)
        print(user_serializer)
        if user_serializer.is_valid(raise_exception=ValueError):
            user = user_serializer.create(validated_data=user_data)
            print(user)
        else:
            print(user_data)
        # Overriding create function necessitates this, can be changed to take ints if preferred.
        team_data = validated_data.get('team')
        player, _ = Player.objects.update_or_create(user=user, team=Team.objects.get(name=team_data['name']))
        return player

class GameKeeperSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(required=True)
    class Meta:
        model = GameKeeper
        fields = [
            "user",
        ]
    def create(self, validated_data):
        user_data = validated_data.get('user')
        user_serializer = UserPostSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=ValueError):
            user = user_serializer.create(validated_data=user_data)
        else:
            print(user_data)
        gamekeeper, _ = GameKeeper.objects.update_or_create(user=user)
        return gamekeeper
