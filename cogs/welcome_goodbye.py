import datetime
import json
import discord
from discord.ext.tasks import loop

import constants

def init():
    try:
        with open('data/inouts_in_a_day.json'):
            pass
    except FileNotFoundError:
        with open('data/inouts_in_a_day.json', 'w') as f:
            now = datetime.datetime.now()
            json.dump({
                'day': now.day,
                'month': now.month,
                'joins': 0,
                'leaves': 0
            }, f)


def cleanup_data(user: int):
    with open('data/catpoints.json') as f:
        catpoints = json.load(f)
    # list of {user_id: str, catpoints: int}

    for i in range(len(catpoints)):
        if catpoints[i]['user_id'] == user:
            catpoints.pop(i)
            break

    with open('data/catpoints.json', 'w') as f:
        json.dump(catpoints, f, indent=4)

    with open('data/chatpoints.json') as f:
        chatpoints = json.load(f)
    # list of {user_id: str, catpoints: int}

    for i in range(len(chatpoints)):
        if chatpoints[i]['user_id'] == user:
            chatpoints.pop(i)
            break

    with open('data/chatpoints.json', 'w') as f:
        json.dump(chatpoints, f, indent=4)

    with open('data/dailymsg.json') as f:
        dailymsg = json.load(f)
    # list of {user_id: str, catpoints: int}

    for i in range(len(dailymsg)):
        if dailymsg[i]['user_id'] == user:
            dailymsg.pop(i)
            break

    with open('data/dailymsg.json', 'w') as f:
        json.dump(dailymsg, f, indent=4)

    with open('data/yearlymsg.json') as f:
        yearlymsg = json.load(f)
    # list of {user_id: str, catpoints: int}

    for i in range(len(yearlymsg)):
        if yearlymsg[i]['user_id'] == user:
            yearlymsg.pop(i)
            break

    with open('data/yearlymsg.json', 'w') as f:
        json.dump(yearlymsg, f, indent=4)


def increment_joins_in_a_day():
    with open('data/inouts_in_a_day.json') as f:
        data = json.load(f)

    now = datetime.datetime.now()
    if data['month'] != now.month and data['day'] != now.day:
        return
    
    data['joins'] += 1

    with open('data/inouts_in_a_day.json', 'w') as f:
        json.dump(f)


def increment_leaves_in_a_day():
    with open('data/inouts_in_a_day.json') as f:
        data = json.load(f)

    now = datetime.datetime.now()
    if data['month'] != now.month and data['day'] != now.day:
        return
    
    data['leaves'] += 1

    with open('data/inouts_in_a_day.json', 'w') as f:
        json.dump(f)


def get_inouts_today():
    with open('data/inouts_in_a_day.json') as f:
        data = json.load(f)

    return data['joins'], data['leaves']


def set_inouts_to_today():
    with open('data/inouts_in_a_day.json') as f:
        data = json.load(f)

    now = datetime.datetime.now()
    if now.day == data['day'] and now.month == data['month']:
        return
    
    data['joins'] = 0
    data['leaves'] = 0

    with open('data/inouts_in_a_day.json', 'w'):
        json.dump(data, f)


class WelcomeGoodbye(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        init()
        self.send_inouts_in_a_day.start()
        super().__init__()

    @discord.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.id in constants.member_banlist:
            try:
                embed = discord.Embed(title=f'You have been banned from {member.guild.name}',
                                      description=f'Reason: [Internal Banlist] Member was found on the internal banlist and was automatically banned', color=discord.Color.red())
                await member.send(embed=embed)
            except discord.Forbidden:
                pass
            await member.ban(reason='[Internal Banlist] Member was found on the internal banlist and was automatically banned')
            return

        channel = self.bot.get_channel(constants.welcome_channel)
        await channel.send(f':green_circle: Welcome {member.display_name} to {member.guild.name}!')
        increment_joins_in_a_day()

    @discord.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.id in constants.member_banlist:
            return

        cleanup_data(member.id)
        channel = self.bot.get_channel(constants.welcome_channel)
        await channel.send(f':red_circle: Goodbye {member.display_name}!')
        increment_leaves_in_a_day()

    @loop(minutes=1)
    async def send_inouts_in_a_day(self):
        now = datetime.datetime.now()
        if now.hour != 0 and now.minute != 0:
            return
    
        joins, leaves = get_inouts_today()
        set_inouts_to_today()
        msg_content = ''
        joins_leaves = ''
        if joins != 0:
            msg_content = f'Today, we saw {joins} {"person" if joins == 1 else "people"} join.'
            joins_leaves = 'Joins'
        if leaves != 0:
            msg_content = f'Today, we saw {leaves} {"person" if leaves == 1 else "people"} leave.'
            joins_leaves = 'Leaves'
        if joins != 0 and leaves != 0:
            msg_content = f'Today, we saw {joins} {"person" if joins == 1 else "people"} join and {leaves} {"person" if leaves == 1 else "people"} leave.'
            joins_leaves = 'Joins/Leaves'

        if msg_content == '':
            return
        embed = discord.Embed(title=f'Today\'s Total {joins_leaves}', description=msg_content, color=discord.Colour.green())
        channel = self.bot.get_channel(constants.welcome_channel)
        await channel.send(embed=embed)
