import json
import logging

import discord
from discord.ext import tasks
import requests
import constants


def init():
    try:
        with open('data/chatpoints.json') as f:
            pass
    except FileNotFoundError:
        with open('data/chatpoints.json', 'w') as f:
            json.dump([], f)


def add_chatpoints(userid: int, chatpoints: int):
    with open('data/chatpoints.json') as f:
        data: list = json.load(f)

    # array of {user_id: int, chatpoints: int}
    for user_data in data:
        if user_data['user_id'] == userid:
            user_data['chatpoints'] += chatpoints
            break
    else:
        data.append({'user_id': userid, 'chatpoints': chatpoints})

    with open('data/chatpoints.json', 'w') as f:
        json.dump(data, f)


def get_chatpoints(userid: int) -> int:
    with open('data/chatpoints.json') as f:
        data = json.load(f)

    # array of {user_id: int, chatpoints: int}
    for user_data in data:
        if user_data['user_id'] == userid:
            return user_data['chatpoints']
    else:
        return 0


def get_chatpoints_leaderboard() -> list:
    with open('data/chatpoints.json') as f:
        data = json.load(f)

    # array of {user_id: int, chatpoints: int}
    return sorted(data, key=lambda x: x['chatpoints'], reverse=True)


def calculate_level(points: int) -> (int, int, int):
    """Calculates some stuff.

    Args:
        points (int): The points to recalculate

    Returns:
        (int, int, int): (current level, xp for next level, xp for last level)
    """
    level = 1
    next_level = 500
    last_level = 0
    while True:
        if points > next_level:
            level += 1
            last_level = next_level
            next_level *= 2
        else:
            break

    return level, next_level, last_level


class ChatPoints(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo.ChatPoints')
        self.bot = bot
        init()
        super().__init__()
        if constants.firebase_url != '':
            self.update_online.start()
        else:
            self.logger.info('Online updater is not running as no Firebase was specified')
        self.logger.info('Initialization successful')

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.type == discord.ChannelType.private:
            return

        old_level, _, _ = calculate_level(get_chatpoints(message.author.id))
        add_chatpoints(message.author.id, len(message.content))
        self.logger.info(f'Added {len(message.content)} ChatPoints to {message.author}')
        current_points = get_chatpoints(message.author.id)
        new_level, next_level_points, last_level_points = calculate_level(current_points)

        if old_level != new_level:
            self.logger.info(f'{message.author} leveled up! {old_level} -> {new_level}')
            channel = self.bot.get_channel(1156628671747080233)
            embed = discord.Embed(title='Level up!',
                                  description=f'{message.author.display_name} leveled up!\n**{old_level}** -> **{new_level}**\n**{current_points - last_level_points}**/**{next_level_points - last_level_points}** till the next level',
                                  color=discord.Color.green())
            await channel.send(content=f'{message.author.mention}', embed=embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def chatpoints(self, ctx: discord.ApplicationContext):
        """Get your ChatPoints amount"""
        self.logger.info(f'{ctx.user} used /chatpoints')
        chatpoints = get_chatpoints(ctx.user.id)
        level, next_level_xp, _ = calculate_level(chatpoints)
        self.logger.info(
            f'{ctx.user} has {chatpoints} ChatPoints (level {level}, {chatpoints}/{next_level_xp} till next level)')
        await ctx.respond(
            f'You have {chatpoints} ChatPoints (level {level}, {chatpoints}/{next_level_xp} till next level)')

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def chatpoint_leaderboard(self, ctx: discord.ApplicationContext):
        """ChatPoints Leaderboard"""
        self.logger.info(f'{ctx.user} used /chatpoint_leaderboard')
        chatpoints = get_chatpoints_leaderboard()
        # show 10 top users
        msg = "# ChatPoints Leaderboard\n"
        for i, user in enumerate(chatpoints[:10]):
            self.logger.info(f'Adding {user["user_id"]} with {user["chatpoints"]} ChatPoints to leaderboard')
            user_obj = await self.bot.fetch_user(user['user_id'])
            msg += f"{i + 1}. {user_obj.display_name} has {user['chatpoints']} ChatPoints\n"
            if i == 9:
                break

        await ctx.respond(msg)
        
        
    @tasks.loop(hours=24)
    async def update_online(self):
        self.logger.info('Uploading ChatPoints leaderboard to Firebase')
        leader_board = get_chatpoints_leaderboard()[:10]
        response = requests.put(f'https://{constants.firebase_url}/discordstats/chatpoints.json', \
            json=leader_board)
        self.logger.info(f'Firebase responded with {response.status_code}')