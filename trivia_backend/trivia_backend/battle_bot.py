import os
import asyncio
from twitchio.ext import commands

class BattleBot(commands.Bot):
    def __init__(self, loop):
        super().__init__(token=os.getenv('TWITCH_BOT_OAUTH'),
                         client_id=os.getenv('TWITCH_BOT_CLIENT_ID'),
                         prefix='!',
                         initial_channels=[])
        self.loop = loop  # Store the loop for later use

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return
        print(f'Received message in {message.channel.name}: {message.content}')

    def start_bot(self):
        self.loop.run_until_complete(self.start())
