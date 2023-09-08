import discord
from discord.ext import tasks


class Status(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        super().__init__()

    @discord.Cog.listener()
    async def on_ready(self):
        self.update_status.start()

    @tasks.loop(minutes=30)
    async def update_status(self):
        guild = self.bot.get_guild(768885442799861821)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'with {guild.member_count} members :3'))
