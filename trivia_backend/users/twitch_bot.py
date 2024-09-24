# users/twitch_bot.py
import os
from twitchio.ext import commands  # Importing the commands module from TwitchIO

class TwitchBot(commands.Bot):
    def __init__(self, channel_name):
        # Initialize the bot using the environment variables for authentication
        super().__init__(
            token=os.getenv('TWITCH_BOT_OAUTH'),  # Bot OAuth token
            client_id=os.getenv('TWITCH_BOT_CLIENT_ID'),  # Bot client ID
            prefix='!',  # Prefix for bot commands
            initial_channels=[channel_name]  # The channel to join, typically the logged-in user's channel
        )

    async def event_ready(self):
        # Called when the bot is connected and ready
        print(f"Bot is online and connected as: {self.nick}")
        print(f"Connected to the following channel(s): {self.connected_channels}")

    async def event_message(self, message):
        # This event is triggered whenever a message is sent in chat
        if message.echo:
            return  # Ignore the bot's own messages to prevent loops

        print(f"Received message from {message.author.name}: {message.content}")

        # Process commands in case the message contains a valid command
        await self.handle_commands(message)

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        # A simple bot command that responds to '!hello'
        await ctx.send(f"Hello, {ctx.author.name}!")

# Function to start the bot
def start_bot(channel_name):
    bot = TwitchBot(channel_name)
    bot.run()

# Function to stop the bot (example implementation)
def stop_bot():
    # Custom logic to stop the bot could be implemented here if needed
    print("Stopping bot...")
