from rest_framework import mixins, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from .models import Images
from .serializer import ImageSerializer
from trashmain.auxillary import get_player_team
from trashmain.permissions import isPlayer, isGameKeeper

"""
For more information about the formatting of the requests, please view the readme
"""


"""
Class that provides an endpoint for users to allow them to submit images to the database.
Can only be accessed by players  
"""
class ImageSubmissionViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Images.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated, isPlayer]
    serializer_class = ImageSerializer

    """
    Function that provides the endpoint with post request functionality. 
    Allows for an image to be submitted and added to the database. 
    """
    def perform_create(self, serializer):
        serializer.save(team=get_player_team(self.request.user))


"""
Class that provides an endpoint that allows users to get a list of all images in the database.
Can only be accessed by gamekeepers
"""
class ImageListViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Images.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated, isGameKeeper]
    serializer_class = ImageSerializer

    """
    Function that provides the endpoint with get request functionality. 
    Allows for a list of all images in the database to be listed.

    Returns:
    self.list() (list) - A list of all images in the database in JSON format   
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


"""
Class that provides an endpoint that allows users to delete an image from the database.
Can only be accessed by gamekeepers 
"""
class ImageDeleteView(APIView):

    permission_classes = [permissions.IsAuthenticated, isGameKeeper]

    """
    Function that provides the endpoint with post request functionality. 
    Allows for an image ID to be sent and then deletes the image with the corresponding
    ID from the database if it exists.

    Returns:
    Response(JSON) (JSON) - Informs the user whether the image was successfully deleted or not  
    """
    def post(self, request):
        id = request.data.get("id", None)
        # Checks if an ID has been obtained, returns 404 if not
        if id is None:
            return Response(
                {"message": "Invalid ID submitted"}, status=status.HTTP_404_NOT_FOUND
            )

        # Try to get and delete an image with the specified ID, returns 404 if not possible
        try:
            image = Images.objects.get(pk=id)
            image.delete()
            return Response(
                {"message": "Image successfully deleted"},
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                {"message": "Image with specified ID does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
