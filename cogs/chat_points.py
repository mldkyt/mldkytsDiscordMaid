import json

import discord


def init():
    try:
        with open('catpoints.json') as f:
            pass
    except FileNotFoundError:
        with open('catpoints.json', 'w') as f:
            json.dump([], f)


def add_chatpoints(userid: int, chatpoints: int):
    with open('chatpoints.json') as f:
        data = json.load(f)

    # array of {user_id: int, chatpoints: int}
    for user_data in data:
        if user_data['user_id'] == userid:
            user_data['chatpoints'] += chatpoints
            break
    else:
        data.append({'user_id': userid, 'chatpoints': chatpoints})

    with open('chatpoints.json', 'w') as f:
        json.dump(data, f)


def get_chatpoints(userid: int) -> int:
    with open('chatpoints.json') as f:
        data = json.load(f)

    # array of {user_id: int, chatpoints: int}
    for user_data in data:
        if user_data['user_id'] == userid:
            return user_data['chatpoints']
    else:
        return 0


def calculate_level(points: int) -> (int, int):
    level = 1
    next_level = 500
    while True:
        if points > next_level:
            level += 1
            next_level *= 2
        else:
            break

    return level, next_level


class ChatPoints(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        init()
        super().__init__()

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        add_chatpoints(message.author.id, len(message.content))

    @discord.slash_command()
    async def chatpoints(self, ctx: discord.ApplicationContext):
        """Get your ChatPoints amount"""
        chatpoints = get_chatpoints(ctx.user.id)
        level, next_level_xp = calculate_level(chatpoints)
        await ctx.respond(f'You have {chatpoints} ChatPoints (level {level}, {chatpoints}/{next_level_xp} till next level)')
