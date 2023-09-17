
import discord
import constants

# log: message delete, message edit, member timeout, member kick and member ban

class EventLogger(discord.Cog):
  def __init__(self, bot: discord.Bot) -> None:
    self.bot = bot
    super().__init__()
  
  @discord.Cog.listener()
  async def on_message_delete(self, message: discord.Message):
    if message.author.bot:
      return
    channel = self.bot.get_channel(constants.log_channel)
    embed = discord.Embed(title='Message Deleted', description=f'{message.author} deleted a message in {message.channel.mention}\nOriginal content:\n\n{message.content}', color=discord.Color.red())
    await channel.send(embed=embed)
    
  @discord.Cog.listener()
  async def on_message_edit(self, before: discord.Message, after: discord.Message):
    if before.author.bot:
      return
    embed = discord.Embed(title='Message Edited', description=f'{before.author} edited a message in {before.channel.mention}\nPrevious content:\n\n{before.content}\n\nAfter content:\n\n{after.content}', color=discord.Color.red())
    channel = self.bot.get_channel(constants.log_channel)
    channel.send(embed=embed)
    
    
  @discord.Cog.listener()
  async def on_member_remove(self, member: discord.Member):
    channel = self.bot.get_channel(constants.log_channel)
    embed = discord.Embed(title='Member Left', description=f'{member} left the server.', color=discord.Color.red())
    await channel.send(embed=embed)
    
  @discord.Cog.listener()
  async def on_member_ban(self, guild: discord.Guild, user: discord.User):
    channel = self.bot.get_channel(constants.log_channel)
    embed = discord.Embed(title='Member Banned', description=f'{user} was banned from the server.', color=discord.Color.red())
    await channel.send(embed=embed)
    
  @discord.Cog.listener()
  async def on_member_unban(self, guild: discord.Guild, user: discord.User):
    channel = self.bot.get_channel(constants.log_channel)
    embed = discord.Embed(title='Member Unbanned', description=f'{user} was unbanned from the server.', color=discord.Color.red())
    await channel.send(embed=embed)
    
  @discord.Cog.listener()
  async def on_member_update(self, before: discord.Member, after: discord.Member):
    if before.nick != after.nick:
      channel = self.bot.get_channel(constants.log_channel)
      await channel.send(f'{before} changed their nickname from {before.nick} to {after.nick}')
    if before.roles != after.roles:
      channel = self.bot.get_channel(constants.log_channel)
      role = None
      for r in before.roles:
        if r not in after.roles:
          role = r
          break
      if role is None:
        for r in after.roles:
          if r not in before.roles:
            role = r
            break
      if role is None:
        return
      embed = discord.Embed(title='Role Update', description=f'{before} changed their roles', color=discord.Color.red())
      embed.add_field(name='Role', value=role.mention)
      embed.add_field(name='Before', value=', '.join([r.name for r in before.roles]))
      embed.add_field(name='After', value=', '.join([r.name for r in after.roles]))
      await channel.send(embed=embed)
      
  @discord.Cog.listener()
  async def on_member_join(self, member: discord.Member):
    channel = self
    embed = discord.Embed(title='Member Joined', description=f'{member} joined the server.', color=discord.Color.red())
    await channel.send(embed=embed)
    
  @discord.Cog.listener()
  async def on_member_timeout(self, member: discord.Member):
    channel = self.bot.get_channel(constants.log_channel)
    embed = discord.Embed(title='Member Timed Out', description=f'{member} was timed out on the server.', color=discord.Color.red())
    await channel.send(embed=embed)
    
  @discord.Cog.listener()
  async def on_member_kick(self, guild: discord.Guild, user: discord.User):
    channel = self.bot.get_channel(constants.log_channel)
    embed = discord.Embed(title='Member Kicked', description=f'{user} was kicked from the server.', color=discord.Color.red())
    await channel.send(embed=embed)