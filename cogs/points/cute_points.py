import json
import logging
import os

from discord.ext import tasks
import discord
import requests
import constants

def init():
    if os.path.exists('data/catpoints.json') and not os.path.exists('data/cutepoints.json'):
        with open('data/cutepoints.json', 'w') as f1:
            with open('data/catpoints.json') as f2:
                f1.write(f2.read())

        os.remove('data/catpoints.json')

    try:
        with open('data/cutepoints.json') as f:
            pass
    except FileNotFoundError:
        with open('data/cutepoints.json', 'w') as f:
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


    @discord.Cog.listener()
    async def on_ready(self):
        if constants.firebase_url != '':
            self.sync_online.start()
            

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
            add_cutepoints(message.author.id, cutepoints)

    @discord.slash_command()
    async def cutepoints_leaderboard(self, ctx: discord.ApplicationContext):
        """Get the CutePoints leaderboard"""
        await ctx.respond('CutePoints have moved here! https://programmerastolfo.github.io/discord/cutepoints')


    @tasks.loop(hours=24)
    async def sync_online(self):
        data = get_cutepoints_leaderboard()[:50]
        data_2 = []
        for i in data:
            member = self.bot.get_guild(constants.guild_id).get_member(i['user_id'])
            i['cutepoints'] = i['catpoints']
            del i['catpoints']
            if member is not None:
                i['name'] = member.display_name
                if member.avatar is not None:
                    i['avatar'] = str(member.avatar.url)
                else:
                    i['avatar'] = 'https://cdn.discordapp.com/embed/avatars/5.png'
                data_2.append(i)
            else:
                i['name'] = f'User({i["user_id"]})'
                i['avatar'] = 'https://cdn.discordapp.com/embed/avatars/5.png'
        requests.put(f'https://{constants.firebase_url}/discordstats/cutepoints.json', \
            json=data_2)

        