# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
import os
from twitchio.ext import commands
import threading
import asyncio

# Keep track of the bot thread
bot_thread = None

# Home view
def home(request):
    return render(request, 'home.html')

# Dashboard view
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'username': request.user.username})

# Logout view - renamed to match the URL pattern
@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('/')

# Function to start the Twitch bot
@login_required
def start_bot_view(request):
    global bot_thread  # Ensure we use the global bot_thread variable
    if request.method == 'POST':
        # Create a Twitch bot using TwitchIO
        class Bot(commands.Bot):
            def __init__(self):
                super().__init__(token=os.getenv('TWITCH_BOT_OAUTH'),
                                 client_id=os.getenv('TWITCH_BOT_CLIENT_ID'),
                                 prefix='!',
                                 initial_channels=[request.user.username])

            async def event_ready(self):
                print(f'Logged in as | {self.nick}')

            async def event_message(self, message):
                if message.echo:
                    return  # Ignore messages sent by the bot itself
                print(f'Received message: {message.content}')

        # Function to start the bot and create the event loop
        def run_bot():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            bot = Bot()
            loop.run_until_complete(bot.start())

        # Run the bot in a separate thread if not already running
        if bot_thread is None or not bot_thread.is_alive():
            bot_thread = threading.Thread(target=run_bot, daemon=True)
            bot_thread.start()

        return redirect('/dashboard/')
    
    return render(request, 'dashboard.html', {'username': request.user.username})

# Function to stop the Twitch bot
@login_required
def stop_bot_view(request):
    global bot_thread  # Ensure we use the global bot_thread variable
    if request.method == 'POST' and bot_thread is not None and bot_thread.is_alive():
        print("Stopping the bot...")
        # Stopping the bot gracefully
        # TwitchIO does not have a built-in stop function,
        # so we might have to exit the thread by other means (e.g., signaling)
        bot_thread.join(timeout=5)
        bot_thread = None
        print("Bot stopped.")

    return redirect('/dashboard/')
