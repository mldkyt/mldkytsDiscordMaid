import datetime

import discord
import requests
from discord.ext import tasks

import constants


class WebsiteSync(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        super().__init__()

    @discord.Cog.listener()
    async def on_ready(self):
        self.sync.start()
        self.sync_members()

    @tasks.loop(hours=24)
    async def sync(self):
        self.sync_members()

    @tasks.loop(minutes=1)
    async def after_femboy(self):
        date = datetime.datetime.now()
        if date.hour == 18 and date.minute == 0 and date.weekday() == 5:
            data = requests.get('https://mldkyt-s-website-default-rtdb.europe-west1.firebasedatabase.app/ff/votes.json').json()
            # array of { ip: string } (ip is the hashed ip address of the voter)
            channel = self.bot.get_channel(constants.private_channel)
            await channel.send(f'{len(data)} headpats for mldkyt on femboy friday! :3')

    def sync_members(self):
        data = {
            'members': len(self.bot.get_guild(constants.guild_id).members),
            'online': len([member for member in self.bot.get_guild(constants.guild_id).members if member.status != discord.Status.offline]),
        }
        requests.put('https://mldkyt-s-website-default-rtdb.europe-west1.firebasedatabase.app/discordstats.json', json=data)
