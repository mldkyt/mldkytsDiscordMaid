import logging
import re

import discord

import constants


class Column3Chat(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo/:3ChannelLimit')
        self.bot = bot
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
