import logging
import discord

import constants


class ChatLimit(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo/ChatLimit')
        self.bot = bot
        super().__init__()
        self.logger.info('Initialization successful')

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id != constants.general_channel:
            return  # only apply to a general channel
        # warn user that their message is about to hit the limit above 800
        if len(message.content) > 800:
            self.logger.info(f'Message from {message.author} is about to hit length limit: {len(message.content)}/1000 characters')
            msg = await message.reply(f'{message.author.mention} your message is about to hit length limit: {len(message.content)}/1000')
            await msg.delete(delay=5)

        # delete if above 1000
        if len(message.content) > 1000:
            self.logger.info(f'Message from {message.author} is too long: {len(message.content)}/1000 characters')
            await message.delete()
            msg = await message.channel.send(f'{message.author.mention} your message is too long! (max 1000 characters)')
            await msg.delete(delay=5)
