
import logging
import discord
import constants

class Testing(discord.Cog):
    def __init__(self) -> None:
        self.logger = logging.getLogger('astolfo.Testing')
        super().__init__()
        if constants.dev_mode:
            self.logger.warn('Running in dev mode!')
            
    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.type == discord.ChannelType.public_thread or \
            message.channel.type == discord.ChannelType.private_thread:
            thread: discord.Thread = message.channel
            await thread.parent.send('test message 1')
            await thread.send('test message 2')
    