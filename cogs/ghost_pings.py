import datetime
import json
import discord
import logging
import constants
import os

def init():
    if not os.path.exists('data/ghost_pings.json'):
        with open('data/ghost_pings.json', 'w') as f:
            json.dump([], f)

def add_message_with_mentions(message: discord.Message) -> None:
    filter_messages()
    logger = logging.getLogger('astolfo/GhostPings')
    with open('data/ghost_pings.json') as f:
        data: list = json.load(f)
        
    data.append({
        'message_id': message.id, 
        'mentions': [m.id for m in message.mentions], 
        'created': message.created_at.timestamp()
    })
    
    with open('data/ghost_pings.json', 'w') as f:
        json.dump(data, f)
        
def is_ghost_ping(message_id: int) -> bool:
    with open('data/ghost_pings.json') as f:
        data: list = json.load(f)
        
    for m in data:
        if m['message_id'] == message_id:
            return True
        
    return False

def filter_messages():
    logger = logging.getLogger('astolfo/GhostPings')
    with open('data/ghost_pings.json') as f:
        data: list = json.load(f)
        
    for m in data:
        if m['created'] < (datetime.datetime.utcnow().timestamp() - 60):
            logger.info('Removing old ghost ping with message ID {}'.format(m['message_id']))
            data.remove(m)
            
    with open('data/ghost_pings.json', 'w') as f:
        json.dump(data, f)



class GhostPings(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo/GhostPings')
        self.bot = bot
        init()
        super().__init__()
        self.logger.info('GhostPings was initialized')
        
    
    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        
        self.logger.info('Message was sent in {} by {} containing {} mentions'.format(msg.channel.name, msg.author.display_name, len(msg.mentions)))
        if len(msg.mentions) == 0:
            return
        
        self.logger.info('Adding message to ghost ping list')
        add_message_with_mentions(msg)
    
    @discord.Cog.listener()
    async def on_message_delete(self, msg: discord.Message):
        if msg.author.bot:
            return
        
        filter_messages()
        if not is_ghost_ping(msg.id):
            return
        
        log_channel = self.bot.get_channel(constants.log_channel)
        log_embed = discord.Embed(
            title='Ghost ping detected!',
            color=discord.Color.red(),
            fields=[
                discord.EmbedField(
                    name='Author',
                    value='<@{}>'.format(msg.author.id)
                ),
                discord.EmbedField(
                    name='Channel',
                    value='<#{}>'.format(msg.channel.id)
                ),
                discord.EmbedField(
                    name='Content',
                    value=msg.content
                )
            ]
        )
        await log_channel.send(embed=log_embed)
        
    