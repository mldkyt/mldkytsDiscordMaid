import datetime
import json
import logging

import discord
from discord.ext import tasks

import constants


def init_messages():
    """Create dailymsg.json if it doesn't exist"""
    try:
        with open('data/yearlymsg.json', 'r') as f:
            pass
    except FileNotFoundError:
        with open('data/yearlymsg.json', 'w') as f:
            json.dump([], f)


def add_message(user: int):
    with open('data/yearlymsg.json', 'r') as f:
        data: list = json.load(f)

    # list of {user_id: int, messages: int}
    for user_data in data:
        if user_data['user_id'] == user:
            user_data['messages'] += 1
            break
    else:
        data.append({'user_id': user, 'messages': 1})

    with open('data/yearlymsg.json', 'w') as f:
        json.dump(data, f)


def get_messages():
    """Get all messages and sort them by messages sent"""
    with open('data/yearlymsg.json', 'r') as f:
        data: list = json.load(f)
    return sorted(data, key=lambda x: x['messages'], reverse=True)


def clear_messages():
    with open('data/yearlymsg.json', 'w') as f:
        json.dump([], f)


class YearlyMessages(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo.YearlyMessages')
        self.bot = bot
        super().__init__()
        self.logger.info('Initialization successful')

    @discord.Cog.listener()
    async def on_ready(self):
        init_messages()
        self.logger.info('Starting clear_messages loop')
        self.clear_messages.start()
        pass

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        add_message(message.author.id)

    @tasks.loop(minutes=1)
    async def clear_messages(self):
        """Check if it's a new year, if so, send top 10 YEARLY talkers and clear the list"""
        time = datetime.datetime.now()
        if time.hour != 0 or time.minute != 0 or time.day != 1 or time.month != 1:
            return
        
        self.logger.info('Sending yearly messages')

        messages = get_messages()
        message_count = 0
        for message in messages:
            message_count += message["messages"]

        msg = '# This year, there were %d messages sent, top chatters:\n' % message_count

        for i, user_data in enumerate(messages):
            self.logger.info(f'User {user_data["user_id"]} has {user_data["messages"]} messages')
            # try to find the user by id, show their display_name if found, else mention
            user = self.bot.get_user(int(user_data['user_id']))
            if user is None:
                username = f'User({user_data["user_id"]})'
            else:
                username = user.display_name
            msg += f'{i + 1}. {username}: {user_data["messages"]} messages\n'
            if i == 9:
                break

        msg += f'# HAPPY NEW YEAR {time.year} EVERYONE!! :3'

        self.logger.info('Sending yearly messages')
        await self.bot.get_channel(constants.general_channel).send(msg)
        clear_messages()
