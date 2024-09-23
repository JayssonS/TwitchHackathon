# trivia_backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trivia/', include('trivia.urls')),  # Include trivia URLs
    path('', include('users.urls')),
]
