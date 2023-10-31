import datetime
import json
import logging

import discord
import requests
from discord.ext import tasks

import constants


class WebsiteSync(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo.WebsiteSync')
        self.bot = bot
        super().__init__()
        self.logger.info('Initialization successful')

    @discord.Cog.listener()
    async def on_ready(self):
        self.logger.info('Starting sync loop')
        self.sync.start()
        self.logger.info('Starting after_femboy loop')
        self.after_femboy.start()
        self.logger.info('Syncing members now')
        self.sync_members()

    @tasks.loop(hours=24)
    async def sync(self):
        self.sync_members()
        await self.sync_bans()

    @tasks.loop(minutes=1)
    async def after_femboy(self):
        date = datetime.datetime.now()
        if date.hour == 18 and date.minute == 0 and date.weekday() == 5:
            data = requests.get(f'https://{constants.firebase_url}/ff/votes.json').json()
            channel = self.bot.get_channel(constants.private_channel)
            await channel.send(f'{len(data)} headpats for Programmer Astolfo on femboy friday! :3')
            requests.put(f'https://{constants.firebase_url}/ff/votes.json', json=[])

    def sync_members(self):
        self.logger.info('Syncing members')
        members = [m for m in self.bot.get_guild(constants.guild_id).members if not m.bot]
        online = [m for m in members if m.status != discord.Status.offline]
        
        self.logger.info('Members: %s, Online: %s', len(members), len(online))
        requests.put(f'https://{constants.firebase_url}/discordstats/members.json', json=len(members))
        requests.put(f'https://{constants.firebase_url}/discordstats/online.json', json=len(online))
        self.logger.info('Members synced')
        
    @discord.Cog.listener()
    async def on_member_ban(self, guild, user):
        self.logger.info('Banned %s, syncing bans', user)
        requests.put(f'https://{constants.firebase_url}/bans/{user.id}.json', json=True)

    async def sync_bans(self):
        self.logger.info('Syncing bans')
        bans = []
        async for i in self.bot.get_guild(constants.guild_id).bans():
            bans.append({
                'user': i.user.display_name,
                'reason': i.reason,
                'id': i.user.id
            })
        
        self.logger.info('Submitting bans to database')    
        requests.put(f'https://{constants.firebase_url}/discordstats/bans.json', json=bans)
        