import datetime
import logging
import os
import discord
import constants

def init():
    # if file not found, create it
    if not os.path.exists('data/bot_commands_time.txt'):
        with open('data/bot_commands_time.txt', 'w') as f:
            time = datetime.datetime.now()
            time -= datetime.timedelta(hours=1)
            f.write(time.strftime('%Y-%m-%d %H:%M:%S.%f'))

def update_message_time() -> bool:
    # update time inside data/bot_commands_time.txt
    # if the time difference from now is more than 1 hour, return True and update the time to now
    # otherwise, return False
    with open('data/bot_commands_time.txt', 'r') as f:
        time = f.read()
        
    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.datetime.now()
    if now - time > datetime.timedelta(hours=1):
        with open('data/bot_commands_time.txt', 'w') as f:
            f.write(now.strftime('%Y-%m-%d %H:%M:%S.%f'))
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
        
        if message.channel.id != constants.commands_channel:
            return
        
        if not update_message_time():
            self.logger.info('Message received in commands channel, but time difference is less than 1 hour')
            return
        
        self.logger.info('Sending message to commands channel')
        await message.channel.send('''# Here are some commands that you can use here:
                                       
L.hug @user - Give a hug to a user
L.kiss @user - Give a kiss to a user
L.cuddle @user - Cuddle with a user
L.pat @user - Pat a user
L.lapsit @user - Sit on a user's lap
L.love @user - Show love to a user
L.marry @user - Marry a user
L.massage @user - Massage a user

L.poke @user - Poke a user
L.bite @user - Bite a user
L.punch @user - Punch a user
L.slap @user - Slap a user

# Some commands from my bot:

/catpoints - Check your CatPoints
/chatpoints - Check your ChatPoints
@bot - Get the help message from the bot''')
    
