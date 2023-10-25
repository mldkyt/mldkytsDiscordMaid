import logging
import random
import re

import discord
from discord.ext import tasks

import constants


class Column3Chat(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.3ChannelLimit')
        self.bot = bot
        if constants.column_3_channel == 0:
            self.logger.warning('Skipping column 3 channel because it is not specified')
            return
        super().__init__()
        self.logger.info(':3 channel limit initialization successful')

    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.channel.id != constants.column_3_channel:
            return

        regex_1 = re.search(r'^:3{1,30}$', msg.clean_content)
        if regex_1 is None:
            await msg.delete()
            await msg.channel.send(f'{msg.author.mention} This channel is only for :3, nothing else.',
                                   delete_after=5)

    @discord.Cog.listener()
    async def on_message_edit(self, old: discord.Message, new: discord.Message):
        if new.author.bot:
            return
        if new.channel.id != constants.column_3_channel:
            return

        regex_1 = re.search(r'^:3{1,30}$', new.clean_content)
        if regex_1 is None:
            await new.delete()
            await new.channel.send(f'{new.author.mention} This channel is only for :3, nothing else.',
                                   delete_after=5)
