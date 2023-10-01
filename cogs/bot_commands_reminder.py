import datetime
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
        self.bot = bot
        init()
        super().__init__()
        
    @discord.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        
        if message.channel.id != constants.commands_channel:
            return
        
        if not update_message_time():
            return
        
        await message.channel.send('''**Here are some commands that you can use here:**
                                       
owo hug @user - Give a hug to a user
owo kiss @user - Give a kiss to a user
owo cuddle @user - Cuddle with a user
owo pat @user - Pat a user

**Some commands from my bot:**

/catpoints - Check your CatPoints
/chatpoints - Check your ChatPoints
@bot - Get the help message from the bot''')
    
