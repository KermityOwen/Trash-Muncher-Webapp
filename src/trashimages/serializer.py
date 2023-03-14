from rest_framework import serializers
from .models import Images

class ImageSerializer(serializers.ModelSerializer):
    """ 
    Used to get specific attributes from the database in JSON format
    """
    class Meta:
        """ 
        Specifies which model the fields will be coming from and the fields extracted
        """
        model = Images
        fields = "__all__"
