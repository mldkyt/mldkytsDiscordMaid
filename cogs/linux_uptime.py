import logging
import os

import discord


class Uptime(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.Uptime')
        self.bot = bot
        super().__init__()
        self.logger.info('Initialization successful')

    @discord.slash_command(guild_ids=[768885442799861821])
    async def uptime(self, ctx: discord.ApplicationContext) -> None:
        self.logger.info('Getting uptime and sending to message')
        uptime = os.popen('uptime -p').read().strip()
        await ctx.respond(uptime)
