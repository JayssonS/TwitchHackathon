from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.db import models
from users.models import TwitchChannel, Friendship, UserProfile
from social_django.utils import load_strategy
from django.views.decorators.http import require_POST
import os
import threading
import asyncio
from trivia_backend.battle_bot import BattleBot
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Keep track of the bot thread
bot_thread = None

# Home view
def home(request):
    return render(request, 'home.html')

# Dashboard view
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'username': request.user.username})

# Logout view
@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('/')

@login_required
def save_twitch_channel(request):
    if request.user.is_authenticated:
        channel_name = request.user.username
        TwitchChannel.objects.update_or_create(
            user=request.user,  # Set the user field to the logged-in user
            defaults={'channel_name': channel_name}
        )
        print(f"Channel '{channel_name}' saved to database with user {request.user}.")
    return redirect('/dashboard/')

# Start the bot when the server starts
def start_bot():
    global bot_thread

    def run_bot():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bot_instance = BattleBot(loop)
        loop.run_until_complete(bot_instance.start())

    if bot_thread is None or not bot_thread.is_alive():
        bot_thread = threading.Thread(target=run_bot, daemon=True, name="TwitchBotThread")
        bot_thread.start()

@login_required
def send_friend_request(request, to_user_id):
    to_user = get_object_or_404(User, id=to_user_id)
    friendship, created = Friendship.objects.get_or_create(from_user=request.user, to_user=to_user)
    
    if not created:
        return JsonResponse({'message': 'Friend request already sent'}, status=400)

    # Notify the recipient of the new friend request via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{to_user.id}",
        {
            "type": "friend_list_update",
            "message": "You have a new friend request!"
        }
    )

    return JsonResponse({'message': 'Friend request sent successfully'}, status=200)

@login_required
def respond_friend_request(request, from_user_id, response):
    friendship = get_object_or_404(Friendship, from_user_id=from_user_id, to_user=request.user)
    
    if response == 'accept':
        friendship.status = 'accepted'
        friendship.save()

        # Notify both users about the accepted friend request
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{friendship.from_user.id}",
            {
                "type": "friend_list_update",
                "message": "Your friend request was accepted!"
            }
        )
        async_to_sync(channel_layer.group_send)(
            f"user_{friendship.to_user.id}",
            {
                "type": "friend_list_update",
                "message": "You have a new friend!"
            }
        )
        
        return JsonResponse({'message': 'Friend request accepted'}, status=200)

    elif response == 'decline':
        friendship.delete()

        # Notify the sender that the request was declined
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{from_user_id}",
            {
                "type": "friend_list_update",
                "message": "Your friend request was declined."
            }
        )
        
        return JsonResponse({'message': 'Friend request declined'}, status=200)

    return JsonResponse({'message': 'Invalid response'}, status=400)


@login_required
def get_friends(request):
    friends = Friendship.objects.filter(to_user=request.user, status='accepted') | Friendship.objects.filter(from_user=request.user, status='accepted')
    friend_list = [
        {
            'id': friend.from_user.id if friend.to_user == request.user else friend.to_user.id,
            'username': friend.from_user.username if friend.to_user == request.user else friend.to_user.username,
            'online': friend.from_user.userprofile.online if friend.to_user == request.user else friend.to_user.userprofile.online,
        }
        for friend in friends
    ]
    return JsonResponse(friend_list, safe=False)

@login_required
def search_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')

        try:
            user = User.objects.get(username__iexact=username)
            if user == request.user:
                return JsonResponse({'status': 'error', 'message': "Nice try bucko"})
            return JsonResponse({'status': 'success', 'username': user.username, 'user_id': user.id})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
        
@login_required
@require_POST
def remove_friend(request, friend_id):
    # Attempt to find the friend relationship
    try:
        friendship = Friendship.objects.get(
            (models.Q(from_user=request.user, to_user_id=friend_id) | models.Q(from_user_id=friend_id, to_user=request.user)),
            status='accepted'
        )
        friendship.delete()
        return JsonResponse({'message': 'Friend removed successfully'}, status=200)
    except Friendship.DoesNotExist:
        return JsonResponse({'message': 'Friendship does not exist'}, status=400)
    
@login_required
def get_pending_requests(request):
    pending_requests = Friendship.objects.filter(to_user=request.user, status='pending').values('from_user_id', 'from_user__username')
    # Rename keys in the response to match expected frontend keys
    data = [{'from_user_id': req['from_user_id'], 'from_username': req['from_user__username']} for req in pending_requests]
    return JsonResponse(data, safe=False)

