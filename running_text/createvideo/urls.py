from django.urls import path
from .views import create_video

urlpatterns = [
    path('runtext/', create_video, name='runtext'),
]