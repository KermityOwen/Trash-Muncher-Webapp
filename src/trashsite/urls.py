from django.urls import path

from . import views

urlpatterns = [
    path('map',views.map),
    path('register', views.register),
    path('login', views.login),
    path('about', views.about),
    path('', views.index, name='index'),
    path('mapselect', views.mapselect),
    path('imageapprove', views.imageapprove),
]