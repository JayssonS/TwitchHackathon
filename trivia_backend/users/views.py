from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import User, Friendship, UserProfile
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from users.models import TwitchChannel
from social_django.utils import load_strategy
import os
import threading
import asyncio
from trivia_backend.battle_bot import BattleBot  # Import BattleBot correctly

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
        # Link the TwitchChannel with the logged-in user
        TwitchChannel.objects.update_or_create(
            user=request.user,  # Set the user field to the logged-in user
            defaults={'channel_name': channel_name}
        )
        print(f"Channel '{channel_name}' saved to database with user {request.user}.")
    return redirect('/dashboard/')

# Start the bot when the server starts
def start_bot():
    global bot_thread  # Ensure we use the global bot_thread variable

    # Function to start the bot and create the event loop
    def run_bot():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        bot_instance = BattleBot(loop)  # Pass the event loop here
        loop.run_until_complete(bot_instance.start())

    # Run the bot in a separate thread if not already running
    if bot_thread is None or not bot_thread.is_alive():
        bot_thread = threading.Thread(target=run_bot, daemon=True, name="TwitchBotThread")
        bot_thread.start()

@login_required
def send_friend_request(request, to_user_id):
    to_user = get_object_or_404(User, id=to_user_id)
    friendship, created = Friendship.objects.get_or_create(from_user=request.user, to_user=to_user)
    if not created:
        return JsonResponse({'message': 'Friend request already sent'}, status=400)
    return JsonResponse({'message': 'Friend request sent successfully'}, status=200)

@login_required
def respond_friend_request(request, from_user_id, response):
    friendship = get_object_or_404(Friendship, from_user_id=from_user_id, to_user=request.user)
    if response == 'accept':
        friendship.status = 'accepted'
        friendship.save()
        return JsonResponse({'message': 'Friend request accepted'}, status=200)
    elif response == 'decline':
        friendship.status = 'declined'
        friendship.save()
        return JsonResponse({'message': 'Friend request declined'}, status=200)
    return JsonResponse({'message': 'Invalid response'}, status=400)

@login_required
def get_friends(request):
    friends = Friendship.objects.filter(to_user=request.user, status='accepted') | Friendship.objects.filter(from_user=request.user, status='accepted')
    friend_list = [{
        'username': friend.from_user.username if friend.to_user == request.user else friend.to_user.username,
        'online': friend.from_user.userprofile.online if friend.to_user == request.user else friend.to_user.userprofile.online,
    } for friend in friends]
    return JsonResponse(friend_list, safe=False)

@login_required
def search_user(request):
    if request.method == 'POST':
        # Get the username from the request
        username = request.POST.get('username')

        # Check if the user exists
        try:
            user = User.objects.get(username=username)
            if user == request.user:
                return JsonResponse({'status': 'error', 'message': "Nice try bucko"})
            return JsonResponse({'status': 'success', 'username': user.username, 'user_id': user.id})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})