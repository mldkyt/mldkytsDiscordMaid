

import logging
import discord
from discord.ext import tasks
import constants

class MemberScan(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.MemberScan')
        self.bot = bot
        super().__init__()
        self.logger.info('MemberScan initialized successfully')
        
    @discord.Cog.listener()
    async def on_ready(self):
        self.logger.info('Starting MemberScan task')
        self.scan_members.start()
        self.logger.info('MemberScan task started successfully')
        
    @tasks.loop(minutes=1)
    async def scan_members(self):
        guild = self.bot.get_guild(constants.guild_id)
        for member in guild.members:
            if member.activity is None:
                continue
            if member.activity.name is None:
                continue
            for word in constants.word_blacklist:
                if word in member.activity.name.lower():
                    embed = discord.Embed(title=f'You have been kicked from {guild.name}',
                                  description=f'Reason: You have a bad word in your current activity!', color=discord.Color.yellow())
                    embed.add_field(name='Get back',
                                    value='https://discord.gg/JgFNmSwYME')
                    embed.add_field(name='The bad word', value=word)
                    try:
                        await member.send(embed=embed)
                    except discord.Forbidden:
                        self.logger.info(f'Could not send DM to {member}, skipping')
                        pass
                    
                    
                    log_embed = discord.Embed(
                        title='Member was automatically kicked',
                        fields=[
                            discord.EmbedField('User', member.display_name, True),
                            discord.EmbedField('Reason', 'Bad word in their activity, the word being %s' % (word), True)
                        ]
                    )
                    
                    log_channel = self.bot.get_channel(constants.log_channel)
                    await log_channel.send(embed=log_embed)
    
