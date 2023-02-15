from rest_framework import serializers
from .models import TrashMonsters

class TMSerializer (serializers.ModelSerializer):
    class Meta:
        model = TrashMonsters
        fields = '__all__'
    
