import datetime
import json
import logging
import os
import discord
import constants
from utils.language import get_string, get_user_lang


def init():
    # if file not found, create it
    if not os.path.exists('data/bot_commands_time.json'):
        with open('data/bot_commands_time.json', 'w') as f:
            json.dump({
                'normal': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                'nsfw': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            }, f)


def update_message_time() -> bool:
    with open('data/bot_commands_time.json', 'r') as f:
        times = json.load(f)

    time = datetime.datetime.strptime(times["normal"], '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.datetime.now()
    if now - time > datetime.timedelta(hours=1):
        times["normal"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        with open('data/bot_commands_time.json', 'w') as f:
            json.dump(times, f)
        return True
    else:
        return False


def update_nsfw_message_time() -> bool:
    with open('data/bot_commands_time.json', 'r') as f:
        times = json.load(f)

    time = datetime.datetime.strptime(times["nsfw"], '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.datetime.now()
    if now - time > datetime.timedelta(hours=1):
        times["nsfw"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        with open('data/bot_commands_time.json', 'w') as f:
            json.dump(times, f)
        return True
    else:
        return False


class BotCommandsReminder(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.BotCommandsReminder')
        self.bot = bot
        init()
        super().__init__()
        self.logger.info('Initialization successful')

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        if message.channel.id == constants.commands_channel and update_message_time():
            self.logger.info('Sending message to commands channel')
            lang = get_user_lang(message.author.id)
            await message.channel.send(get_string('bot_commands_reminder', lang))
            return

        if message.channel.id == constants.nsfw_commands_channel and update_nsfw_message_time():
            self.logger.info('Sending message to commands channel')
            lang = get_user_lang(message.author.id)
            await message.channel.send(get_string('nsfw_bot_commands_reminder', lang))
            return
