
import logging
import discord
import constants

# log: message delete, message edit, member timeout, member kick and member ban

class EventLogger(discord.Cog):
  def __init__(self, bot: discord.Bot) -> None:
    self.logger = logging.getLogger('astolfo.EventLogger')
    self.bot = bot
    super().__init__()
    self.logger.info('Initialization successful')
  
  @discord.Cog.listener()
  async def on_message_delete(self, message: discord.Message):
    if message.author.bot:
      return
    self.logger.info(f'Message from {message.author} deleted in {message.channel.mention}')
    channel = self.bot.get_channel(constants.log_channel)
    embed = discord.Embed(title='Message Deleted', description=f'{message.author} deleted a message in {message.channel.mention}\nOriginal content:\n\n{message.content}', color=discord.Color.red())
    await channel.send(embed=embed)
    
  @discord.Cog.listener()
  async def on_message_edit(self, before: discord.Message, after: discord.Message):
    if after.author.bot:
      return
    self.logger.info(f'Message from {before.author} edited in {before.channel.mention}')
    embed = discord.Embed(title='Message Edited', description=f'{before.author} edited a message in {before.channel.mention}\nPrevious content:\n\n{before.content}\n\nAfter content:\n\n{after.content}', color=discord.Color.yellow())
    channel = self.bot.get_channel(constants.log_channel)
    await channel.send(embed=embed)
    
  @discord.Cog.listener()
  async def on_member_remove(self, member: discord.Member):
    self.logger.info(f'{member} left the server')
    channel = self.bot.get_channel(constants.log_channel)
    embed = discord.Embed(title='Member Left', description=f'{member} left the server.', color=discord.Color.red())
    await channel.send(embed=embed)
    
  @discord.Cog.listener()
  async def on_member_ban(self, guild: discord.Guild, user: discord.User):
    self.logger.info(f'{user} was banned from the server')
    channel = self.bot.get_channel(constants.log_channel)
    embed = discord.Embed(title='Member Banned', description=f'{user} was banned from the server.', color=discord.Color.red())
    await channel.send(embed=embed)
    
  @discord.Cog.listener()
  async def on_member_unban(self, guild: discord.Guild, user: discord.User):
    self.logger.info(f'{user} was unbanned from the server')
    channel = self.bot.get_channel(constants.log_channel)
    embed = discord.Embed(title='Member Unbanned', description=f'{user} was unbanned from the server.', color=discord.Color.red())
    await channel.send(embed=embed)
    
  @discord.Cog.listener()
  async def on_member_update(self, before: discord.Member, after: discord.Member):
    if before.nick != after.nick:
      self.logger.info(f'{before} changed their nickname from {before.nick} to {after.nick}')
      channel = self.bot.get_channel(constants.log_channel)
      embed = discord.Embed(title='Nickname Update', description=f'{before} changed their nickname', color=discord.Color.red())
      embed.add_field(name='Before', value=before.nick, inline=False)
      embed.add_field(name='After', value=after.nick, inline=False)
      await channel.send(embed=embed)
      
  @discord.Cog.listener()
  async def on_member_join(self, member: discord.Member):
    self.logger.info(f'{member} joined the server')
    channel = self.bot.get_channel(constants.log_channel)
    embed = discord.Embed(title='Member Joined', description=f'{member} joined the server.', color=discord.Color.red())
    await channel.send(embed=embed)
    
  @discord.Cog.listener()
  async def on_member_timeout(self, member: discord.Member):
    self.logger.info(f'{member} was timed out on the server')
    channel = self.bot.get_channel(constants.log_channel)
    embed = discord.Embed(title='Member Timed Out', description=f'{member} was timed out on the server.', color=discord.Color.red())
    await channel.send(embed=embed)
    
  @discord.Cog.listener()
  async def on_member_kick(self, guild: discord.Guild, user: discord.User):
    self.logger.info(f'{user} was kicked from the server')
    channel = self.bot.get_channel(constants.log_channel)
    embed = discord.Embed(title='Member Kicked', description=f'{user} was kicked from the server.', color=discord.Color.red())
    await channel.send(embed=embed)