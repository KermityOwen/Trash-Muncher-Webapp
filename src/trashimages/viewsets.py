from rest_framework import mixins, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from .models import Images
from .serializer import ImageSerializer
from trashmain.auxillary import get_player_team
from trashmain.permissions import isPlayer

# Create your views here.
class ImageSubmissionViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Images.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated, isPlayer]
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        serializer.save(team=get_player_team(self.request.user))


class ImageListViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Images.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ImageSerializer


class ImageDeleteView(APIView):
    def get(self, request):
        ids = request.data.get("id")
        ids.split(',')
        images = Images.objects.filter(id__in=ids)
        serialized_images = ImageSerializer(images)
        return Response(serialized_images.data)

    # Function to delete a list of images from the database 
    def delete(self, request):
        ids = request.query_params.get("ids")
        if ids:
            for id in ids.split(','):
                id = int(id)
                image = Images.objects.get(id=id)
                image.delete()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
