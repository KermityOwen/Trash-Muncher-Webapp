from rest_framework import mixins, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import TrashImages
from .serializer import ImageSerializer
from trashmain.auxillary import get_player_team
from trashmain.permissions import isPlayer

# Create your views here.
class ImageSubmissionViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = TrashImages.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated, isPlayer]
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        serializer.save(team=get_player_team(self.request.user))


class ImageListViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = TrashImages.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ImageSerializer

