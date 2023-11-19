
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


    @discord.slash_command(guild_ids=[constants.guild_id])
    @cooldown(1, 10, BucketType.default)
    async def brimo(self, ctx: discord.ApplicationContext, amt: int):
        if amt > 25000000:
            await ctx.respond(get_string('brimo_command_character_limit', get_user_lang(ctx.user.id)))
        elif amt > 2000:
            await ctx.defer()
            
        os.system('./thing.sh')
            
        if amt > 2000:
            with open('msg.txt') as f:
                msg = f.read()[:amt]
            with open('msg.txt', 'w') as f:
                f.write(msg)
            await ctx.followup.send(file=discord.File('msg.txt'))
        else:
            with open('msg.txt') as f:
                msg = f.read()[:amt]
            await ctx.respond(msg)
