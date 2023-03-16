from rest_framework import serializers
from .models import TrashMonsters


class TMSerializer(serializers.ModelSerializer):
    """ 
    Used to get specific attributes from the database in JSON format
    """
    class Meta:
        """ 
        Specifies which model the fields will be coming from and the fields extracted
        """
        model = TrashMonsters
        fields = "__all__"


class TMIDSerializer(serializers.ModelSerializer):
    """ 
    Used to get specific attributes from the database in JSON format
    """
    class Meta:
        """ 
        Specifies which model the fields will be coming from and the fields extracted
        """
        model = TrashMonsters
        fields = ["TM_ID"]