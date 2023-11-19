
import logging

import discord

import constants

from utils.language import get_string, get_user_lang


class OwoChannelLimit(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.OwoChannelLimit')
        self.bot = bot
        if constants.owo_uwu_channel == 0:

            return
        super().__init__()

        
    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.channel.id != constants.owo_uwu_channel:
            return
        if msg.content.lower() != 'owo' and msg.content.lower() != 'uwu':
            await msg.delete()
            lang = get_user_lang(msg.author.id)
            await msg.channel.send(get_string('owo_channel_limit', lang) % (msg.author.mention), delete_after=5)
            
    @discord.Cog.listener()
    async def on_message_edit(self, old: discord.Message, new: discord.Message):
        if new.author.bot:
            return
        if new.channel.id != constants.owo_uwu_channel:
            return
        if new.content.lower() != 'owo' and new.content.lower() != 'uwu':
            await new.delete()
            lang = get_user_lang(new.author.id)
            await new.channel.send(get_string('owo_channel_limit', lang) % (new.author.mention), delete_after=5)
