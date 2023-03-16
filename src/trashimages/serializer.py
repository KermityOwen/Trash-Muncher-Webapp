from rest_framework import serializers
from django.core.files.base import ContentFile
import base64
from .models import Images
from trashusers.models import Team
from trashmonsters.models import TrashMonsters
from uuid import uuid4


def base64_to_img(data):
        format, img_str = data.split(';base64,')
        name, ext = format.split('/')
        return ContentFile(base64.b64decode(img_str + "=="), name=uuid4().hex + "." + ext)


class ImageSerializer(serializers.ModelSerializer):
    """ 
    Used to get specific attributes from the database in JSON format
    """

    class Meta:
        """ 
        Specifies which model the fields will be coming from and the fields extracted
        """
        model = Images
        fields = ["id", "b64_img", "image", "team","monster"]

    

    def create(self, validated_data):
        img_data = validated_data.get("b64_img")

        img = base64_to_img(img_data)
        team_data = validated_data.get("team")
        monster_data = validated_data.get("monster")
        image, created = Images.objects.update_or_create(
            image=img, team=team_data, monster=monster_data)
        return image
