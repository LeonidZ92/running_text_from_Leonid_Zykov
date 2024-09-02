from django.urls import path
from .views import index, create_video

urlpatterns = [
    path('', index, name='index'),
    path('create_video/', create_video, name='create_video'),
]
