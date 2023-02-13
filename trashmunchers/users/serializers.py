from django.contrib.auth import get_user_model
from .models import Player, GameKeeper, Team
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name')        


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    team = TeamSerializer(required=True)

    class Meta:
        model = Player
        fields = [
            "user",
            "team",
        ]
class GamekeeperSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = GameKeeper
        fields = [
            "user",
        ]


class PlayerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        read_only_fields = ["id"]
        fields = ["email", "first_name", "last_name", "password"]
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
