
import logging
import discord
import constants
import random
from discord.ext import tasks


class OwoChannelLimit(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo/OwoChannelLimit')
        self.bot = bot
        self.send_random.start()
        self.logger.info('Started OwO random sending task')
        super().__init__()
        self.logger.info('OwO channel limit initialization successful')
        
    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.channel.id != constants.owo_uwu_channel:
            return
        if msg.content.lower() != 'owo' or msg.content.lower() != 'uwu':
            await msg.delete()
            await msg.channel.send(f'{msg.author.mention} This channel is only for OwO and UwU, nothing else~ :3', delete_after=5)
            
    @tasks.loop(minutes=1)
    async def send_random(self):
        if random.randint(0, 250) != 250:
            return
        
        channel = self.bot.get_channel(constants.owo_uwu_channel)
        variant = random.randint(1, 2)
        if variant == 1:
            await channel.send('owo')
        elif variant == 2:
            await channel.send('uwu')