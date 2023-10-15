
import datetime
import logging
import discord
import constants

class TimeCommand(discord.Cog):
  def __init__(self, bot: discord.Bot) -> None:
    self.logger = logging.getLogger('astolfo.TimeCommand')
    self.bot = bot
    super().__init__()
    self.logger.info('Initialization successful')
    
  @discord.slash_command(guild_ids=[constants.guild_id])
  async def time(self, ctx: discord.ApplicationContext):
    self.logger.info('Getting time and sending to message')
    utc_time = datetime.datetime.now()
    programmer_astolfo_time = utc_time + datetime.timedelta(hours=2)
    await ctx.respond(f'UTC Time (Server): {utc_time.strftime("%H:%M")} ({utc_time.strftime("%I:%M %p")})\nProgrammer Astolfo\'s time: {programmer_astolfo_time.strftime("%H:%M")} ({programmer_astolfo_time.strftime("%I:%M %p")})')
  
