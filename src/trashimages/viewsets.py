from rest_framework import mixins, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle

from .models import Images
from .serializer import ImageSerializer
from trashmain.auxillary import get_player_team
from trashmain.permissions import isPlayer, isGameKeeper

"""
For more information about the formatting of the requests, please view the readme
"""


class ImageSubmissionViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Provides an endpoint for users to allow them to submit images to the database.
    Can only be accessed by players
    """
    queryset = Images.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    
    # Only allow authenticated players to use this endpoint
    permission_classes = [permissions.IsAuthenticated, isPlayer]

    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        """
        Provides the endpoint with post request functionality.
        Allows for an image to be submitted and added to the database.
        """
        serializer.save(team=get_player_team(self.request.user))


class ImageListViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Provides an endpoint that allows users to get a list of all images in the database.
    Can only be accessed by gamekeepers
    """

    queryset = Images.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    # Only allow authenticated gamekeepers to use this endpoint
    permission_classes = [permissions.IsAuthenticated, isGameKeeper]
    serializer_class = ImageSerializer

    def get(self, request, *args, **kwargs):
        """
        Provides the endpoint with get request functionality.
        Allows for a list of all images in the database to be listed.

        Returns:
        self.list() (list) - A list of all images in the database in JSON format
        """
        return self.list(request, *args, **kwargs)


class ImageDeleteView(APIView):
    """
    Provides an endpoint that allows users to delete an image from the database.
    Can only be accessed by gamekeepers
    """

    # Only allow authenticated gamekeepers to use this endpoint 
    permission_classes = [permissions.IsAuthenticated, isGameKeeper]

    def post(self, request):
        """
        Provides the endpoint with post request functionality.
        Allows for an image ID to be sent and then deletes the image with the corresponding
        ID from the database if it exists.

        Returns:
        Response(JSON) (JSON) - Informs the user whether the image was successfully deleted or not
        """
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
