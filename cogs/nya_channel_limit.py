import discord
import re
import logging
import constants

class NyaChannelLimit(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo/NyaChannelLimit')
        self.bot = bot
        super().__init__()
        self.logger.info('Nyaa channel limit initialization successful')
        
    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.channel.id != constants.nya_channel:
            return
        regex_1 = re.search(r'^[Nn][y]+[a]+[h]*[~]?(\s+[;:][3]+)?$', msg.clean_content)
        regex_2 = re.search(r'^[Mm][e]+[r]+[o]?[w]?[~]?(\s+[;:][3])?$', msg.clean_content)
        if regex_1 is None and regex_2 is None:
            await msg.delete()
            await msg.channel.send(f'{msg.author.mention} This channel is only for meowing, nothing else.', delete_after=5)
        
    
