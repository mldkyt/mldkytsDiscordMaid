import datetime
import json
import logging
import os
import discord
import constants


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
            await message.channel.send('''# Here are some commands that you can use here:

            L.arrest - Arrest another user
            L.baka - When somebody behaves like a baka
            L.bite - Bite another user
            L.bonk - Send someone to horny jail
            L.cuddle - Cuddle another user
            L.highfive - Give another user a high five
            L.hug - Hug another user
            L.kiss - Kiss another user
            L.lapsit - Sit on the lap of another user
            L.lick - Lick another user
            L.love - Love another user
            L.marry - Marry another user
            L.massage - Massage another user
            L.merkel - Merkel another user
            L.pat - Pat another user
            L.poke - Poke another user
            L.punch - Punch another user
            L.reward - Rewards someone with a strawberry
            L.slap - Slap another user
            L.squish - Squish another user
            L.steal - Steal from user
            L.throw - Throw something at another user
            L.tickle - Tickle another user
            L.wave - Wave your hands at someone
            L.yeet - Yeet another user
            
            # Some commands from my bot:

            /catpoints - Check your CatPoints
            /chatpoints - Check your ChatPoints
            @bot - Get the help message from the bot''')
            return

        if update_nsfw_message_time():
            self.logger.info('Sending message to commands channel')
            await message.channel.send('''# (18+)Here are some commands that you can use here:

            L.69 - Perform 69 with another user
            L.assfuck - Ass fuck another user
            L.assgrab - Grab someone's ass
            L.blowjob - Give someone a blowjob
            L.bondage - Do lewd bondage stuff with someone
            L.boobsgrab - Grab someone's boobs
            L.boobsuck - Suck someone's boobs
            L.creampie - Give another user a creampie
            L.cum - Cum on someone
            L.dickride - Ride someone's dick
            L.facesit - Sit on someone's face
            L.finger - Finger another user
            L.footjob - Give someone a footjob
            L.fuck - Fuck another user
            L.furryfuck - Fuck someone furry style
            L.handjob - Give someone a handjob
            L.leash - Put another user on a leash
            L.masturbate - Jerk someone off
            L.pussyeat - Eat someone's pussy
            L.spank - Spank another user
            L.strip - Get naked with someone
            L.tittyfuck - Titty fuck another user
            L.yaoifuck - Fuck someone yaoi style
            L.yurifuck - Fuck someone yuri style
            
            # Some commands from my bot:

            /catpoints - Check your CatPoints
            /chatpoints - Check your ChatPoints
            @bot - Get the help message from the bot''')
            return
