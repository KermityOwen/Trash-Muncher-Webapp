from django.urls import path

from . import views

urlpatterns = [
    path('map',views.map),
    path('about', views.about),
    path('', views.index, name='index'),
]
