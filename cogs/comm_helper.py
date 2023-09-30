import json
import os
import discord

language_channels = [
    1157767734831095848,
    1157767678468051175,
    1157767876078473266,
    1157770518901043291,
    1157771769294377101,
    1157772190159225033,
    1157772248485204038
]

all_language_channel = 1147557081721872474


def init():
    if os.path.exists('data/reply_list.json'):
        return
    
    with open('data/reply_list.json', 'w') as f:
        f.write('[]')

def add_to_reply_list(msg: discord.Message, resent: discord.Message):
    with open('data/reply_list.json', 'r') as f:
        data: list = json.load(f)
        
    data.append({
        'language_channel_id': msg.channel.id,
        'original_message_id': msg.id,
        'resent_message_id': resent.id
    })
    
    with open('data/reply_list.json', 'w') as f:
        json.dump(data, f)
        
        
def is_in_reply_list(id: int) -> bool:
    with open('data/reply_list.json', 'r') as f:
        data: list = json.load(f)
        
    for item in data:
        if item['resent_message_id'] == id:
            return True
        
    return False


def get_reply_info(id: int) -> dict:
    with open('data/reply_list.json', 'r') as f:
        data: list = json.load(f)
        
    for item in data:
        if item['resent_message_id'] == id:
            return item
        
    return None


class CommHelper(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        init()
        super().__init__()
        
    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        
        if msg.channel.id in language_channels:
            # resend to all language channel
            msg_content = f'**From {msg.channel.name} by {msg.author.display_name}**: {msg.content}'
            
            if len(msg.attachments) > 0:
                msg_content += f'\n\n### Attachments ({len(msg.attachments)}):'
                for attachment in msg.attachments:
                    msg_content += f'\n{attachment.url}'
                    
            if len(msg.embeds) > 0:
                msg_content += f'\n\n### Message contains {len(msg.embeds)} embed(s) which have been sent with this message.'
            
            resent = await self.bot.get_channel(all_language_channel).send(msg_content, embeds=msg.embeds)
            add_to_reply_list(msg, resent)
            
        if msg.channel.id == all_language_channel and msg.reference is not None and is_in_reply_list(msg.reference.message_id):
            data = get_reply_info(msg.reference.message_id)
            channel = self.bot.get_channel(data['language_channel_id'])
            msg2 = await channel.fetch_message(data['original_message_id'])
            
            msg_content = f'**From {msg.channel.name} by {msg.author.display_name}**: {msg.content}'
            
            if len(msg.attachments) > 0:
                msg_content += f'\n\n### Attachments ({len(msg.attachments)}):'
                for attachment in msg.attachments:
                    msg_content += f'\n{attachment.url}'
                    
            if len(msg.embeds) > 0:
                msg_content += f'\n\n### Message contains {len(msg.embeds)} embed(s) which have been sent with this message.'
                
            await msg2.reply(msg_content, embeds=msg.embeds)
        
    