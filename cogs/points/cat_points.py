import json
import logging

import discord


def init():
    try:
        with open('data/catpoints.json') as f:
            pass
    except FileNotFoundError:
        with open('data/catpoints.json', 'w') as f:
            logger = logging.getLogger('astolfo.CatPoints')
            logger.info('Creating data/catpoints.json')
            json.dump([], f)


def add_catpoints(userid: int, catpoints: int):
    with open('data/catpoints.json') as f:
        data = json.load(f)

    # array of {user_id: int, catpoints: int}
    for user_data in data:
        if user_data['user_id'] == userid:
            user_data['catpoints'] += catpoints
            break
    else:
        data.append({'user_id': userid, 'catpoints': catpoints})

    with open('data/catpoints.json', 'w') as f:
        json.dump(data, f)


def get_catpoints(userid: int) -> int:
    with open('data/catpoints.json') as f:
        data = json.load(f)

    # array of {user_id: int, catpoints: int}
    for user_data in data:
        if user_data['user_id'] == userid:
            return user_data['catpoints']
    else:
        return 0


def get_catpoints_leaderboard() -> list:
    with open('data/catpoints.json') as f:
        data = json.load(f)

    # array of {user_id: int, catpoints: int}
    return sorted(data, key=lambda x: x['catpoints'], reverse=True)


class CatPoints(discord.Cog):

    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo.CatPoints')
        self.bot = bot
        init()
        super().__init__()
        self.logger.info('Initialization successful')

    @discord.slash_command()
    async def catpoints(self, ctx: discord.ApplicationContext):
        """Get your CatPoints amount"""
        await ctx.respond(f'You have {get_catpoints(ctx.user.id)} CatPoints')

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        # count the amount of :3, add 1 catpoint for each
        if message.author.bot:
            return
        if message.channel.type == discord.ChannelType.private:
            return

        catpoints = message.content.count('>:3') * 2
        catpoints += message.content.replace('>:3', '').count(':3')
        catpoints += message.content.count(':#')
        catpoints += message.content.count(';3')
        catpoints += message.content.count('にゃ')
        catpoints += message.content.count('nya')
        catpoints += message.content.count('meow')
        catpoints += message.content.count('mrow')
        catpoints += message.content.count('mrrr')
        if catpoints > 0:
            self.logger.info(f'Adding {catpoints} CatPoints to {message.author}')
        add_catpoints(message.author.id, catpoints)

    @discord.slash_command()
    async def catpoints_leaderboard(self, ctx: discord.ApplicationContext):
        """Get the CatPoints leaderboard"""
        self.logger.info('Getting CatPoints leaderboard')
        leaderboard = get_catpoints_leaderboard()
        msg = "# CatPoints Leaderboard\n"
        for i, user_data in enumerate(leaderboard):
            user = await self.bot.fetch_user(user_data['user_id'])
            self.logger.info(f'Adding {user.display_name} with {user_data["catpoints"]} CatPoints to leaderboard')
            msg += f"{i + 1}. {user.display_name} has {user_data['catpoints']} CatPoints\n"
            if i == 9:
                break

        await ctx.respond(msg)
