# users/routing.py
from django.urls import path
from .consumers import FriendConsumer

websocket_urlpatterns = [
    path('ws/friends/<str:username>/', FriendConsumer.as_asgi()),
]
