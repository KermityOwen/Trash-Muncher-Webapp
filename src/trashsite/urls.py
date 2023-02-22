from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('map',views.map),
    path('mapselect', views.mapselect),
    path('imageapprove', views.imageapprove)
]
