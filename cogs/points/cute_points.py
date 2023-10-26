import json
import logging
import os

from discord.ext import tasks
import discord
import requests
import constants

def init():
    if os.path.exists('data/catpoints.json') and not os.path.exists('data/cutepoints.json'):
        logging.getLogger('astolfo.CutePoints').info('Updating catpoints.json to cutepoints.json')
        with open('data/cutepoints.json', 'w') as f1:
            with open('data/catpoints.json') as f2:
                f1.write(f2.read())

        os.remove('data/catpoints.json')

    try:
        with open('data/cutepoints.json') as f:
            pass
    except FileNotFoundError:
        with open('data/cutepoints.json', 'w') as f:
            logger = logging.getLogger('astolfo.CutePoints')
            logger.info('Creating data/cutepoints.json')
            json.dump([], f)


def add_cutepoints(userid: int, cutepoints: int):
    with open('data/cutepoints.json') as f:
        data = json.load(f)

    for user_data in data:
        if user_data['user_id'] == userid:
            user_data['catpoints'] += cutepoints
            break
    else:
        data.append({'user_id': userid, 'catpoints': cutepoints})

    with open('data/cutepoints.json', 'w') as f:
        json.dump(data, f)


def get_cutepoints(userid: int) -> int:
    with open('data/cutepoints.json') as f:
        data = json.load(f)

    for user_data in data:
        if user_data['user_id'] == userid:
            return user_data['catpoints']
    else:
        return 0


def get_cutepoints_leaderboard() -> list:
    with open('data/cutepoints.json') as f:
        data = json.load(f)

    return sorted(data, key=lambda x: x['catpoints'], reverse=True)


class CutePoints(discord.Cog):

    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo.CutePoints')
        self.bot = bot
        init()
        super().__init__()
        if constants.firebase_url != '':
            self.logger.info('Starting sync_online loop')
            self.sync_online.start()
        else:
            self.logger.info('Not syncing online users because no Firebase was provided')
        self.logger.info('Initialization successful')

    @discord.slash_command()
    async def cutepoints(self, ctx: discord.ApplicationContext):
        """Get your CutePoints amount"""
        await ctx.respond(f'You have {get_cutepoints(ctx.user.id)} CutePoints')

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        # count the amount of :3, add 1 catpoint for each
        if message.author.bot:
            return
        if message.channel.type == discord.ChannelType.private:
            return

        cutepoints = message.content.count('>:3') * 2
        cutepoints += message.content.replace('>:3', '').count(':3')
        cutepoints += message.content.count(':#')
        cutepoints += message.content.count(';3')
        cutepoints += message.content.count('にゃ')
        cutepoints += message.content.count('ニャー')
        cutepoints += message.content.count('nya')
        cutepoints += message.content.count('meow')
        cutepoints += message.content.count('mrow')
        cutepoints += message.content.count('mrrr')
        cutepoints += message.content.count('~')
        if cutepoints > 0:
            self.logger.info(f'Adding {cutepoints} CutePoints to {message.author}')
        add_cutepoints(message.author.id, cutepoints)

    @discord.slash_command()
    async def cutepoints_leaderboard(self, ctx: discord.ApplicationContext):
        """Get the CutePoints leaderboard"""
        self.logger.info('Getting CutePoints leaderboard')
        leaderboard = get_cutepoints_leaderboard()
        msg = "# CutePoints Leaderboard\n"
        for i, user_data in enumerate(leaderboard):
            user = await self.bot.fetch_user(user_data['user_id'])
            self.logger.info(f'Adding {user.display_name} with {user_data["catpoints"]} CutePoints to leaderboard')
            msg += f"{i + 1}. {user.display_name} has {user_data['catpoints']} CutePoints\n"
            if i == 9:
                break

        await ctx.respond(msg)


    @tasks.loop(hours=24)
    async def sync_online(self):
        self.logger.info('Uploading CutePoints leaderboard to Firebase')
        data = get_cutepoints_leaderboard()[:10]
        requests.put(f'https://{constants.firebase_url}/discordstats/cutepoints.json', \
            json=data)
        self.logger.info('CutePoints leaderboard synced')
        