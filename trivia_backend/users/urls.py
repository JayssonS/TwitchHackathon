# users/urls.py
from django.urls import path, include
from . import views
from .views import start_bot_view, stop_bot_view

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('start-bot/', start_bot_view, name='start_bot'),
    path('stop-bot/', stop_bot_view, name='stop_bot'),  # Make sure this line is here
]
