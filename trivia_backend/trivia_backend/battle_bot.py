import os
import asyncio
from twitchio.ext import commands
from asgiref.sync import sync_to_async

class BattleBot(commands.Bot):
    def __init__(self, loop):
        super().__init__(token=os.getenv('TWITCH_BOT_OAUTH'),
                         client_id=os.getenv('TWITCH_BOT_CLIENT_ID'),
                         prefix='!',
                         initial_channels=[])
        self.loop = loop  # Store the loop for later use

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        
        # Fetch channels from the database asynchronously
        channels = await sync_to_async(self.get_channels)()
        
        # Print fetched channels for debugging
        print(f"Fetched channels from database: {channels}")
        
        # Join the fetched channels
        for channel in channels:
            if channel:  # Check if channel is not an empty string
                print(f"Joining channel: {channel}")
                await self.join_channels([channel])

    async def event_message(self, message):
        if message.echo:
            return
        print(f'Received message in {message.channel.name}: {message.content}')

    def start_bot(self):
        self.loop.run_until_complete(self.start())

    def get_channels(self):
        # Import the model within the method to ensure apps are loaded
        from users.models import TwitchChannel
        # Fetch all Twitch channels from your database
        channels = list(TwitchChannel.objects.values_list('channel_name', flat=True))
        print(f"Channels retrieved in get_channels: {channels}")  # Debugging statement
        return channels
