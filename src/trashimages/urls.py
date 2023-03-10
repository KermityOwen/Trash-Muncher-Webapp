from django.urls import path
from . import viewsets
from rest_framework.routers import SimpleRouter

app_name = "TrashMunchers Images"

urlpatterns = [
    path("delete-image/", viewsets.ImageDeleteView.as_view()),
]

img_router = SimpleRouter()
img_router.register(r"submit-image", viewsets.ImageSubmissionViewset, basename="images")
img_router.register(r"list-images", viewsets.ImageListViewset, basename="images")

urlpatterns += img_router.urls
