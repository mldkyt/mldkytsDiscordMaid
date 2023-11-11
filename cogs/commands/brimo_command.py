
import logging
import os
import discord
import constants
from utils.language import get_string, get_user_lang
from discord.ext.commands import cooldown, BucketType

class BrimoCommand(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.BrimoCommand')
        self.bot = bot
        super().__init__()
        self.logger.info('Initialization successful')

    @discord.slash_command(guild_ids=[constants.guild_id])
    @cooldown(1, 10, BucketType.guild)
    async def brimo(self, ctx: discord.ApplicationContext, amt: int):
        if amt > 1024:
            lang = get_user_lang(ctx.author.id)
            await ctx.respond(get_string('brimo_command_character_limit', lang=lang))
            return
        
        os.system('./thing.sh')
        with open('msg.txt') as f:
            msg = f.read()[:amt]
            await ctx.respond(msg)
