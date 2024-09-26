from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
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
