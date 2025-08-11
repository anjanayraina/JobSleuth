import discord
from helper.config import ConfigSingleton
from helper.logger import Logger


class DiscordFetcher:
    def __init__(self, message_limit=100):
        config = ConfigSingleton()
        self.bot_token = config.discord_bot_token
        self.channel_ids = config.discord_channel_ids
        self.message_limit = message_limit
        self.log = Logger(__name__)

        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        self.client = discord.Client(intents=intents)

    async def fetch_messages(self):

        if not self.bot_token or not self.channel_ids:
            self.log.warning("Discord bot token or channel IDs are not configured. Skipping fetch.")
            return []

        try:
            await self.client.login(self.bot_token)
            self.log.info("Discord client logged in successfully.")

            all_messages = []
            for channel_id in self.channel_ids:
                try:
                    channel = await self.client.fetch_channel(channel_id)
                    self.log.info(f"Fetching messages from channel: #{channel.name}")

                    # Iterate through the channel's history
                    async for message in channel.history(limit=self.message_limit):
                        if message.content and not message.author.bot:
                            # Construct a direct link to the message
                            message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"

                            all_messages.append({
                                "text": message.content,
                                "date": message.created_at,
                                "source": "Discord",
                                "url": message_link
                            })
                except discord.NotFound:
                    self.log.error(f"Channel with ID {channel_id} not found.")
                except discord.Forbidden:
                    self.log.error(f"Bot does not have permissions to read history in channel ID {channel_id}.")
                except Exception as e:
                    self.log.error(f"An error occurred fetching from channel {channel_id}: {e}")

            return all_messages

        finally:
            if self.client.is_ready():
                await self.client.close()
                self.log.info("Discord client connection closed.")