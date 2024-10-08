import os
import threading
import asyncio
from django.core.wsgi import get_wsgi_application

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trivia_backend.settings')

# Create the WSGI application object
application = get_wsgi_application()

# Start the Twitch bot automatically
def start_bot():
    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Import BattleBot here to avoid premature access to Django's ORM
        from trivia_backend.battle_bot import BattleBot
        bot = BattleBot(loop)  # Pass the loop when initializing BattleBot
        bot.start_bot()

    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run, daemon=True, name="TwitchBotThread")
    bot_thread.start()

# Start the bot when the server starts
start_bot()
