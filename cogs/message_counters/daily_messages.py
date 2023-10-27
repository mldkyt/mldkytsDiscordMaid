import datetime
import json
import logging
import os

import discord
from discord.ext import tasks

import constants


def init_messages():
    """Create dailymsg.json if it doesn't exist"""
    try:
        with open('data/dailymsg.json') as f:
            pass
    except FileNotFoundError:
        with open('data/dailymsg.json', 'w') as f:
            json.dump([], f)


def add_message(user: int):
    with open('data/dailymsg.json') as f:
        data: list = json.load(f)

    # list of {user_id: int, messages: int}
    for user_data in data:
        if user_data['user_id'] == user:
            user_data['messages'] += 1
            break
    else:
        data.append({'user_id': user, 'messages': 1})

    with open('data/dailymsg.json', 'w') as f:
        json.dump(data, f)


def get_messages():
    """Get all messages and sort them by messages sent"""
    with open('data/dailymsg.json') as f:
        data: list = json.load(f)
    return sorted(data, key=lambda x: x['messages'], reverse=True)


def clear_messages():
    with open('data/dailymsg.json', 'w') as f:
        json.dump([], f)


def save_messages_to_history():
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)
    with open('data/dailymsg.json') as f:
        data: list = json.load(f)
        
    # create folder data/messages_daily_history if it doesn't exist
    if not os.path.exists('data/messages_daily_history'):
        os.makedirs('data/messages_daily_history')
    
    with open(f'data/messages_daily_history/{yesterday.day}-{yesterday.month}-{yesterday.year}.json', 'w') as f:
        json.dump(data, f)
        

class DailyMessages(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo.DailyMessages')
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
        
    @discord.slash_command()
    async def test_save_messages_to_history(self, ctx: discord.ApplicationContext):
        save_messages_to_history()
        await ctx.respond('Saved messages to history', ephemeral=True)

    @tasks.loop(minutes=1)
    async def clear_messages(self):
        """Check if it's midnight, if so, send top 5 chatters and clear the list"""
        time = datetime.datetime.now()
        if time.hour != 0 or time.minute != 0:
            return
        
        self.logger.info('Clearing messages and sending top 5 chatters')

        save_messages_to_history()
        messages = get_messages()
        message_count = 0
        for message in messages:
            message_count += message["messages"]

        msg = "# Today, there were %d sent messages:\n" % message_count

        for i, user_data in enumerate(messages):
            # try to find the user by id, show their display_name if found, else mention
            user = self.bot.get_user(int(user_data['user_id']))
            if user is None:
                username = f'User({user_data["user_id"]})'
            else:
                username = user.display_name
            msg += f'{i + 1}. {username}: {user_data["messages"]} messages\n'
            self.logger.info(f'Adding {username} with {user_data["messages"]} messages to top 5 chatters')
            if i == 4:
                break

        await self.bot.get_channel(constants.general_channel).send(msg)
        clear_messages()
