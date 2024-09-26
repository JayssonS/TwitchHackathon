# trivia_backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # Include the URLs from your 'users' app
    path('auth/', include('social_django.urls', namespace='social')),  # Add this line
]
