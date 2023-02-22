from rest_framework import serializers
from .models import TrashImages


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrashImages
        fields = '__all__'