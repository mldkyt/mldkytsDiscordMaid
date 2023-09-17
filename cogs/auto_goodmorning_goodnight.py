
from discord.ext import tasks
import datetime
import discord
import constants


class AutoGoodMorningGoodNight(discord.Cog):
  def __init__(self, bot: discord.Bot) -> None:
    self.bot = bot
    super().__init__()
    
  @discord.Cog.listener()
  async def on_ready(self):
    self.auto_good_morning.start()
    self.auto_good_night.start()
    self.auto_good_afternoon.start()
    self.auto_good_midnight.start()
    
  @tasks.loop(hours=1)
  async def auto_good_morning(self):
    time = datetime.datetime.now()
    if time.hour == 8:
      general = self.bot.get_channel(constants.general_channel)
      await general.send('I wish everyone a good morning :3')
      
  @tasks.loop(hours=1)
  async def auto_good_night(self):
    time = datetime.datetime.now()
    if time.hour == 20:
      general = self.bot.get_channel(constants.general_channel)
      await general.send('I wish everyone a good night :3')
      
  # afternoon and midnight
  @tasks.loop(hours=1)
  async def auto_good_afternoon(self):
    time = datetime.datetime.now()
    if time.hour == 14:
      general = self.bot.get_channel(constants.general_channel)
      await general.send('I wish everyone a good afternoon :3')
      
  @tasks.loop(hours=1)
  async def auto_good_midnight(self):
    time = datetime.datetime.now()
    if time.hour == 0:
      general = self.bot.get_channel(constants.general_channel)
      await general.send('I wish everyone a good midnight :3')