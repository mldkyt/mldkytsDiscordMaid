import logging
import discord
from discord.ext import tasks

import constants


class Status(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo/Status')
        self.bot = bot
        super().__init__()
        self.logger.info('Initialization successful')

    @discord.Cog.listener()
    async def on_ready(self):
        self.logger.info('Starting update_status loop')
        self.update_status.start()

    @tasks.loop(minutes=30)
    async def update_status(self):
        self.logger.info('Updating status')
        guild = self.bot.get_guild(constants.guild_id)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'with {guild.member_count} members :3'))
        self.logger.info('Status updated')
