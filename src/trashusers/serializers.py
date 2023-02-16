from django.contrib.auth import get_user_model
from .models import Player, GameKeeper, Team
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

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
    user = UserPostSerializer(required=True)
    # team = TeamSerializer(required=True)

    class Meta:
        model = Player
        fields = [
            "user"
        ]
    def create(self, validated_data):
        user_data = validated_data['user']
        user_serializer = UserPostSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=ValueError):
            user = user_serializer.create(validated_data=user_data)
        else:
            print(user_data)
        # team_data = validated_data.pop('team')
        # team = TeamSerializer.create(TeamSerializer(), validated_data=team_data)
        print("REACHED HERE 1")
        player = Player.objects.update_or_create(user=user) #, team=team
        print("REACHED HERE 2")
        return player

class GameKeeperSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(required=True)
    class Meta:
        model = GameKeeper
        fields = [
            "user",
        ]
    def create(self, validated_data):
        user_data = validated_data['user']
        user_serializer = UserPostSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=ValueError):
            user = user_serializer.create(validated_data=user_data)
        else:
            print(user_data)
        gamekeeper = GameKeeper.objects.update_or_create(user=user)
        return gamekeeper
