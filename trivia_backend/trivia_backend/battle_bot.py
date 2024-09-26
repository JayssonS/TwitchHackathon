import os
import asyncio
import logging  # Import the logging module
from twitchio.ext import commands
from asgiref.sync import sync_to_async

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BattleBot(commands.Bot):
    def __init__(self, loop):
        super().__init__(token=os.getenv('TWITCH_BOT_OAUTH'),
                         client_id=os.getenv('TWITCH_BOT_CLIENT_ID'),
                         prefix='!',
                         initial_channels=[])
        self.loop = loop

    async def event_ready(self):
        logger.info(f'Logged in as | {self.nick}')
        
        # Fetch channels from the database asynchronously
        channels = await sync_to_async(self.get_channels)()
        
        # Log fetched channels for debugging
        logger.info(f"Fetched channels from database: {channels}")
        
        # Join the fetched channels
        for channel in channels:
            if channel:
                logger.info(f"Joining channel: {channel}")
                await self.join_channels([channel])

    async def event_message(self, message):
        if message.echo:
            return
        logger.info(f'Received message in {message.channel.name}: {message.content}')

    def start_bot(self):
        self.loop.run_until_complete(self.start())

    def get_channels(self):
        from users.models import TwitchChannel
        channels = list(TwitchChannel.objects.values_list('channel_name', flat=True))
        logger.info(f"Channels retrieved in get_channels: {channels}")  # Log the retrieved channels
        return channels
