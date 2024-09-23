# users/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Add the home view
    path('auth/', include('social_django.urls', namespace='social')),
    path('dashboard/', views.dashboard, name='dashboard'),
]
