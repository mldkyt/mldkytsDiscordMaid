import datetime
import json
import logging
import discord
from discord.ext.tasks import loop

import os
import constants


def init():    
    if not os.path.exists('data/inouts_in_a_day.json'):
        with open('data/inouts_in_a_day.json', 'w') as f:
            now = datetime.datetime.now()
            json.dump({
                'day': now.day,
                'month': now.month,
                'joins': 0,
                'leaves': 0
            }, f)


def increment_joins_in_a_day():
    with open('data/inouts_in_a_day.json') as f:
        data = json.load(f)

    now = datetime.datetime.now()
    if data['month'] != now.month and data['day'] != now.day:
        return

    data['joins'] += 1

    with open('data/inouts_in_a_day.json', 'w') as f:
        json.dump(data, f)


def increment_leaves_in_a_day():
    with open('data/inouts_in_a_day.json') as f:
        data = json.load(f)

    now = datetime.datetime.now()
    if data['month'] != now.month or data['day'] != now.day:
        return

    data['leaves'] += 1

    with open('data/inouts_in_a_day.json', 'w') as f:
        json.dump(data, f)


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
    
    if not os.path.exists('data/inout_history'):
        os.mkdir('data/inout_history')
        
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    with open(f'data/inout_history/{yesterday.month}-{yesterday.day}-{yesterday.year}.json', 'w') as f:
        json.dump(data, f)

    data['day'] = now.day
    data['month'] = now.month
    data['joins'] = 0
    data['leaves'] = 0

    with open('data/inouts_in_a_day.json', 'w') as f:
        json.dump(data, f)


class WelcomeGoodbye(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.WelcomeGoodbye')
        self.bot = bot
        init()
        self.send_inouts_in_a_day.start()
        super().__init__()


    @discord.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        
        channel = self.bot.get_channel(constants.welcome_channel)
        await channel.send(f':green_circle: Welcome {member.display_name} to {member.guild.name}!')
        increment_joins_in_a_day()

    @discord.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        kicked = False
        banned = False



        async for entry in member.guild.audit_logs(limit=10, action=discord.AuditLogAction.kick):
            if entry.target == member:
                kicked = True

        async for entry in member.guild.audit_logs(limit=10, action=discord.AuditLogAction.ban):
            if entry.target == member:
                banned = True

        goodbye_message = f':red_circle: Goodbye {member.name}!'
        if kicked:
            goodbye_message = f'⚠️ {member.name} was kicked!'
        if banned:
            goodbye_message = f'❌ {member.name} was banned!'

        channel = self.bot.get_channel(constants.welcome_channel)

        await channel.send(goodbye_message)
        increment_leaves_in_a_day()

    @loop(minutes=1)
    async def send_inouts_in_a_day(self):
        now = datetime.datetime.now()
        if now.hour != 0 or now.minute != 0:
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


        embed = discord.Embed(title=f'Today\'s Total {joins_leaves}', description=msg_content,
                              color=discord.Colour.green())
        channel = self.bot.get_channel(constants.welcome_channel)
        await channel.send(embed=embed)
        