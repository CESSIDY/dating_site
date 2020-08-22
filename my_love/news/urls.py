from django.urls import path
from .views import (
    newsGenerate,
    chat,
    room
)

urlpatterns = [
    path('generate', newsGenerate, name='news'),
    path('', chat, name='chat'),
    path('<str:room_name>/', room, name='room'),
]