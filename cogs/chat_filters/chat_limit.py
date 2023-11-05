import logging
import discord

import constants
from utils.language import get_string, get_user_lang

class ChatLimit(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo.ChatLimit')
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
        lang = get_user_lang(message.author.id)
        if len(message.content) > 800:
            self.logger.info(
                f'Message from {message.author} is about to hit length limit: {len(message.content)}/1000 characters')
            msg = await message.reply(get_string('chat_limit_about_to_hit', lang) % (message.author.mention, str(len(message.content))))
            await msg.delete(delay=5)

        # delete if above 1000
        if len(message.content) > 1000:
            self.logger.info(f'Message from {message.author} is too long: {len(message.content)}/1000 characters')
            await message.delete()
            msg = await message.channel.send(get_string('chat_limit_too_long', lang) % (message.author.mention))
            await msg.delete(delay=5)
