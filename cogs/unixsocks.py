
import logging
import os
import discord
import requests
from discord.ext.commands import cooldown

import constants
import discord.ext.tasks


def get_version():
    with open('changelog.md') as f:
        return f.read().split('\n')[0].split(' ')[2]
    

class UnixSocks(discord.Cog):

    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.UnixSocks')
        self.bot = bot
        super().__init__()
        self.logger.info('Initialization successful')
        
    @discord.Cog.listener()
    async def on_ready(self):
        self.logger.info('Starting auto_unixsocks loop')
        self.auto_unixsocks.start()

    @discord.slash_command(guild_ids=[constants.guild_id])
    @cooldown(1, 10, discord.ext.commands.BucketType.guild)
    async def unixsocks(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        
        self.logger.info('[command] Getting unixsocks and sending to message')
        response = requests.get('https://reddit.com/r/unixsocks/random.json', headers={
            'User-Agent': f'mldkbot/{get_version()}'
        }).json()
        self.logger.info('[command] Got unixsocks')
        first_post = response[0]['data']['children'][0]['data']
        self.logger.info('[command] First post: %s', first_post['title'])
        self.logger.info('[command] First post URL: %s', first_post['url'])
        # download the image and send it as attachment
        image = requests.get(first_post['url'], headers={
            'User-Agent': f'mldkbot/{get_version()}',
            'Accept': 'image/png'
        }).content
        self.logger.info('[command] Downloaded image')
        
        with open('a.png', 'wb') as f:
            f.write(image)

        self.logger.info('[command] Sending message')
        await ctx.followup.send(content=f'[{first_post["title"]}](<https://reddit.com/{first_post["permalink"]}>)', file=discord.File('a.png'))
        
        self.logger.info('[command] Message sent, deleting image')
        os.remove('a.png')
        self.logger.info('[command] Image deleted')
        self.logger.info('[command] Command finished')
        
    @discord.ext.tasks.loop(hours=1)
    async def auto_unixsocks(self):
        self.logger.info('[auto] Getting unixsocks and sending to message')
        response = requests.get('https://reddit.com/r/unixsocks/random.json', headers={
            'User-Agent': f'mldkbot/{get_version()}'
        }).json()
        self.logger.info('[auto] Got unixsocks')
        first_post = response[0]['data']['children'][0]['data']
        self.logger.info('[auto] First post: %s', first_post['title'])
        self.logger.info('[auto] First post URL: %s', first_post['url'])
        # download the image and send it as attachment
        image = requests.get(first_post['url'], headers={
            'User-Agent': f'mldkbot/{get_version()}',
            'Accept': 'image/png'
        }).content
        self.logger.info('[auto] Downloaded image')
        
        with open('a.png', 'wb') as f:
            f.write(image)
            
        self.logger.info('[auto] Sending message')
        channel = self.bot.get_channel(constants.femboy_media_channel)
        await channel.send(content=f'[{first_post["title"]}](<https://reddit.com/{first_post["permalink"]}>)', file=discord.File('a.png'))
        
        self.logger.info('[auto] Message sent, deleting image')
        os.remove('a.png')
        self.logger.info('[auto] Image deleted')
        self.logger.info('[auto] Automatic finished')
        
