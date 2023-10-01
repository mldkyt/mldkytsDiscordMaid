import os
import discord

class Uptime(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        super().__init__()
        
    @discord.slash_command(guild_ids=[768885442799861821])
    async def uptime(self, ctx: discord.ApplicationContext) -> None:
        uptime = os.popen('uptime -p').read().strip()
        await ctx.respond(uptime)