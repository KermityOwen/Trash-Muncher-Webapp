from rest_framework import serializers
from .models import Images

""" 
Class that used to get specific attributes from the database in JSON format
"""
class ImageSerializer(serializers.ModelSerializer):
    """ 
    Class that specifies which model the fields will be coming from and the fields extracted
    """
    class Meta:
        model = Images
        fields = "__all__"
