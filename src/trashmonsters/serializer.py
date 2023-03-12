from rest_framework import serializers
from .models import TrashMonsters

""" 
Class that used to get specific attributes from the database in JSON format
"""
class TMSerializer(serializers.ModelSerializer):
    """ 
    Class that specifies which model the fields will be coming from and the fields extracted
    """
    class Meta:
        model = TrashMonsters
        fields = "__all__"
