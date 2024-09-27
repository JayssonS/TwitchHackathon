from django.urls import path, include
from .views import send_friend_request, respond_friend_request, get_friends
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search_user/', views.search_user, name='search_user'),
    path('logout/', views.logout_view, name='logout'),
    path('save_twitch_channel/', views.save_twitch_channel, name='save_twitch_channel'),
    path('send_friend_request/<int:to_user_id>/', send_friend_request, name='send_friend_request'),
    path('respond_friend_request/<int:from_user_id>/<str:response>/', respond_friend_request, name='respond_friend_request'),
    path('get_friends/', get_friends, name='get_friends'),
]
