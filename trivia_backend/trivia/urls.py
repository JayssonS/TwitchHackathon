# trivia/urls.py
from django.urls import path
from .views import fetch_trivia

urlpatterns = [
    path('fetch/', fetch_trivia, name='fetch_trivia'),
]
