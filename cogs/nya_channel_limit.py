import random
import discord
from discord.ext import tasks
import re
import logging
import constants

class NyaChannelLimit(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo/NyaChannelLimit')
        self.bot = bot
        self.send_random.start()
        self.logger.info('Started Nyaa random sending task')
        super().__init__()
        self.logger.info('Nyaa channel limit initialization successful')
        
    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.channel.id != constants.nya_channel:
            return
        regex_1 = re.search(r'^[Nn][y]+[a]+[h]*[~]?(\s+[;:][3]+)?$', msg.clean_content)
        regex_2 = re.search(r'^[Mm][er]+[o]?[w]?[~]?(\s+[;:][3])?$', msg.clean_content)
        if regex_1 is None and regex_2 is None:
            await msg.delete()
            await msg.channel.send(f'{msg.author.mention} This channel is only for meowing, nothing else.', delete_after=5)
        
    @discord.Cog.listener()
    async def on_message_edit(self, old: discord.Message, new: discord.Message):
        if new.author.bot:
            return
        if new.channel.id != constants.nya_channel:
            return
        regex_1 = re.search(r'^[Nn][y]+[a]+[h]*[~]?(\s+[;:][3]+)?$', new.clean_content)
        regex_2 = re.search(r'^[Mm][er]+[o]?[w]?[~]?(\s+[;:][3])?$', new.clean_content)
        if regex_1 is None and regex_2 is None:
            await new.delete()
            await new.channel.send(f'{new.author.mention} This channel is only for meowing, nothing else.', delete_after=5)
        
    @tasks.loop(minutes=1)
    async def send_random(self):
        if random.randint(0, 250) != 250:
            return
        
        channel = self.bot.get_channel(constants.nya_channel)
        variant = random.randint(1, 2)
        if variant == 1:
            amount = random.randint(1, 10)
            amount_2 = random.randint(1, 5)
            ending = random.randint(1, 2)
            tildie = random.randint(1, 2)
            h = random.randint(1, 2)
            
            message = 'ny' + 'a' * amount
            if h == 2:
                message += 'h'
            if tildie == 2:
                message += '~'
            if ending == 2:
                message += ' :' + '3' * amount_2
                
            await channel.send(message)
        elif variant == 2:
            variant_2 = random.randint(1, 2)
            if variant_2 == 1:
                tildie = random.randint(1, 2)
                ending = random.randint(1, 2)
                amount_2 = random.randint(1, 5)
                message = 'Meow'
                if tildie == 2:
                    message += '~'
                if ending == 2:
                    message += ' :' + '3' * amount_2
                
                await channel.send(message)
            elif variant_2 == 2:
                amount = random.randint(1, 10)
                amount_2 = random.randint(1, 5)
                ending = random.randint(1, 2)
                tildie = random.randint(1, 2)
                
                message = 'm' + 'r' * amount
                if tildie == 2:
                    message += '~'
                if ending == 2:
                    message += ' :' + '3' * amount_2
                    
                await channel.send(message)