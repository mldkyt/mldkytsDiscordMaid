
import datetime
import discord
import constants

class TimeCommand(discord.Cog):
  def __init__(self, bot: discord.Bot) -> None:
    self.bot = bot
    super().__init__()
    
  @discord.slash_command(guild_ids=[constants.guild_id])
  async def time(self, ctx: discord.ApplicationContext):
    utc_time = datetime.datetime.now()
    mld_time = utc_time + datetime.timedelta(hours=2)
    await ctx.respond(f'UTC Time (Server): {utc_time.strftime("%H:%M")} ({utc_time.strftime("%I:%M %p")})\nProgrammer Astolfo\'s time: {mld_time.strftime("%H:%M")} ({mld_time.strftime("%I:%M %p")})')
  
