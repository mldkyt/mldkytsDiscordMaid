import logging
import re

import discord

import constants
from utils.language import get_string, get_user_lang


class NyaChannelLimit(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.NyaChannelLimit')
        self.bot = bot
        if constants.nya_channel == 0:
            self.logger.warning('Skipping NyaChannelLimit module because the channel isn\'t specified')
            return
        super().__init__()
        self.logger.info('Nyaa channel limit initialization successful')

    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.channel.id != constants.nya_channel:
            return
        regex_1 = re.search(r'^[Nn][y]+[a]+[h]*[~]?(\s+[;:][3]+)?$', msg.clean_content)
        regex_2 = re.search(r'^[Mm][er]+[o]?[wp]?[~]?(\s+[;:][3])?$', msg.clean_content)
        if regex_1 is None and regex_2 is None:
            await msg.delete()
            lang = get_user_lang(msg.author.id)
            await msg.channel.send(get_string('nya_channel_limit', lang) % (msg.author.mention),
                                   delete_after=5)

    @discord.Cog.listener()
    async def on_message_edit(self, old: discord.Message, new: discord.Message):
        if new.author.bot:
            return
        if new.channel.id != constants.nya_channel:
            return
        regex_1 = re.search(r'^[Nn][y]+[a]+[h]*[~]?(\s+[;:][3]+)?$', new.clean_content)
        regex_2 = re.search(r'^[Mm][er]+[o]?[wp]?[~]?(\s+[;:][3])?$', new.clean_content)
        if regex_1 is None and regex_2 is None:
            await new.delete()
            lang = get_user_lang(new.author.id)
            await new.channel.send(get_string('nya_channel_limit', lang) % (new.author.mention),
                                   delete_after=5)
