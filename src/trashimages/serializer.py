from rest_framework import serializers
from django.core.files.base import ContentFile
import base64
from .models import Images
from trashusers.models import Team
from trashmonsters.models import TrashMonsters
from trashmonsters.serializer import TMIDSerializer
from trashusers.serializers import TeamSerializer
from uuid import uuid4


def base64_to_img(data):
        format, img_str = data.split(';base64,')
        name, ext = format.split('/')
        return ContentFile(base64.b64decode(img_str + "=="), name=uuid4().hex + "." + ext)


class ImageSerializer(serializers.ModelSerializer):
    """ 
    Used to get specific attributes from the database in JSON format
    """
    monster = TMIDSerializer(required=True)
    class Meta:
        """ 
        Specifies which model the fields will be coming from and the fields extracted
        """
        model = Images
        fields = ["id", "b64_img", "image", "team","monster"]

    

    def create(self, validated_data):
        """ 
        Gets the information from the post request and uses it to create an Images
        to allow for images to be sent within forms

        Parameters:
        validated_data - POST request sent by the user in JSON format

        Returns: 
        image - Image object created with the data from the POST request 
        """
        
        # Get the relevant data needed to create the model from the request
        img_data = validated_data.get("b64_img")
        team_data = validated_data.get("team")
        monster_data = validated_data.get("monster")

        # Convert the base64 string to an image
        img = base64_to_img(img_data)
        image, created = Images.objects.update_or_create(
            image=img, team=team_data, monster=TrashMonsters.objects.get(TM_ID=monster_data["TM_ID"]))
        return image