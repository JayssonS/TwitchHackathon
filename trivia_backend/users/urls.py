# users/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]
