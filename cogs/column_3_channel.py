import logging
import random
import re

import discord
from discord.ext import tasks

import constants


class Column3Chat(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo/:3ChannelLimit')
        self.bot = bot
        self.send_random.start()
        self.logger.info('Starting :3 random sending task')
        super().__init__()
        self.logger.info(':3 channel limit initialization successful')

    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.channel.id != constants.column_3_channel:
            return

        regex_1 = re.search(r'^:3+$', msg.clean_content)
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

        regex_1 = re.search(r'^:3+$', new.clean_content)
        if regex_1 is None:
            await new.delete()
            await new.channel.send(f'{new.author.mention} This channel is only for :3, nothing else.',
                                   delete_after=5)
            
    @tasks.loop(minutes=1)
    async def send_random(self):
        if random.randint(0, 250) != 250:
            return
        
        amount = random.randint(1, 10)
        channel = self.bot.get_channel(constants.column_3_channel)
        await channel.send(':' + '3' * amount)
