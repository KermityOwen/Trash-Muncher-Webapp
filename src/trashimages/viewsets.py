from rest_framework import mixins, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from .models import Images
from .serializer import ImageSerializer
from trashmain.auxillary import get_player_team
from trashmain.permissions import isPlayer, isGameKeeper

# Create your views here.
class ImageSubmissionViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Allows users that are players to add an image to the database
    """
    queryset = Images.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated, isPlayer]
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        serializer.save(team=get_player_team(self.request.user))


class ImageListViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Allows a gamekeeper to view all images currently in the database
    """
    queryset = Images.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated, isGameKeeper]
    serializer_class = ImageSerializer


class ImageDeleteView(APIView):
    """
    Post function to allow the gamekeeper to delete an image with a specified ID 
    """
    permission_classes = [permissions.IsAuthenticated, isGameKeeper]
    def post(self, request):
        id = request.data.get("id", None)
        # Checks if an ID has been obtained, returns 404 if not
        if id is None:
            return Response(
                {
                "message":"Invalid ID submitted"
                }, status=status.HTTP_404_NOT_FOUND)
        
        # Try to get and delete an image with the specified ID, returns 404 if not possible
        try:
            image = Images.objects.get(pk=id)
            image.delete()
            return Response({
                "message":"Image successfully deleted"
            },
            status=status.HTTP_200_OK,)
        except:
            return Response(
                {
                "message":"Image with specified ID does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )

            
