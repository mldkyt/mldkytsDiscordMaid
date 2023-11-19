
import datetime
import logging
import os
import discord
import constants
from utils.language import get_string, get_user_lang


def init():
    if not os.path.exists('data/dailyfunfacttime.txt'):
        with open('data/dailyfunfacttime.txt', 'w') as f:
            now = datetime.datetime.now()
            f.write(now.strftime('%s'))
            

def passed():
    with open('data/dailyfunfacttime.txt') as f:
        data = f.read()
    data = int(data)
    now = datetime.datetime.now()
    return now.timestamp() - data > 86400

def update_time():
    if not passed():
        return
    
    with open('data/dailyfunfacttime.txt', 'w') as f:
        now = datetime.datetime.now()
        f.write(now.strftime('%s'))


class DailyFunFactLimit(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.DailyFunFactLimit')
        self.bot = bot
        init()
        super().__init__()

        
    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.channel.id != constants.daily_fun_fact_channel:
            return
        
        if passed():
            update_time()
            return
        
        await msg.delete()
        lang = get_user_lang(msg.author.id)
        await msg.channel.send(get_string('You can only send one fun fact per day!', lang), delete_after=5)
