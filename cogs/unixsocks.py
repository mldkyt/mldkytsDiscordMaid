
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
        self.bot = bot
        super().__init__()
        
    @discord.Cog.listener()
    async def on_ready(self):
        self.auto_unixsocks.start()

    @discord.slash_command(guild_ids=[constants.guild_id])
    @cooldown(1, 10, discord.ext.commands.BucketType.guild)
    async def unixsocks(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        
        response = requests.get('https://reddit.com/r/unixsocks/random.json', headers={
            'User-Agent': f'ProgrammerAstolfoBot/{get_version()}'
        }).json()
        first_post = response[0]['data']['children'][0]['data']
        # download the image and send it as attachment
        image = requests.get(first_post['url'], headers={
            'User-Agent': f'ProgrammerAstolfoBot/{get_version()}',
            'Accept': 'image/png'
        }).content
        
        with open('a.png', 'wb') as f:
            f.write(image)

        await ctx.followup.send(content=f'[{first_post["title"]}](<https://reddit.com/{first_post["permalink"]}>)', file=discord.File('a.png'))
        
    @discord.ext.tasks.loop(hours=1)
    async def auto_unixsocks(self):
        response = requests.get('https://reddit.com/r/unixsocks/random.json', headers={
            'User-Agent': f'ProgrammerAstolfoBot/{get_version()}'
        }).json()
        first_post = response[0]['data']['children'][0]['data']
        # download the image and send it as attachment
        image = requests.get(first_post['url'], headers={
            'User-Agent': f'ProgrammerAstolfoBot/{get_version()}',
            'Accept': 'image/png'
        }).content
        
        with open('a.png', 'wb') as f:
            f.write(image)

        channel = self.bot.get_channel(constants.femboy_media_channel)
        await channel.send(content=f'[{first_post["title"]}](<https://reddit.com/{first_post["permalink"]}>)', file=discord.File('a.png'))
        
