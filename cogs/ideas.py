import json
import logging
import discord
from discord.ui.input_text import InputText
from discord.ui.item import Item
import os
import constants

def init():
    if os.path.exists('data/ideas.json'):
        return

    with open('data/ideas.json', 'w') as f:
        json.dump([], f)


def add_idea(type: str, user_id: int, idea: str):
    with open('data/ideas.json') as f:
        data: list = json.load(f)

    data.append({'type': type, 'user_id': user_id, 'idea': idea})

    with open('data/ideas.json', 'w') as f:
        json.dump(data, f)
        
        
def get_ideas():
    with open('data/ideas.json') as f:
        data: list = json.load(f)
        
    return data
        
        
class Ideas(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo/Ideas')
        self.bot = bot
        init()
        super().__init__()
        self.logger.info('Initialization successful')
        
    @discord.slash_command(guild_ids=[768885442799861821])
    async def ideas(self, ctx: discord.ApplicationContext) -> None:
        if ctx.user.id != constants.bot_maintainer:
            self.logger.warning(f'{ctx.user.id} tried to use the ideas command, but does not have permission to do so!')
            await ctx.respond('You do not have permission to use this command!', ephemeral=True)
            return
        
        data = get_ideas()
        if len(data) == 0:
            self.logger.info('There are no ideas submitted yet!')
            await ctx.respond('There are no ideas submitted yet!', ephemeral=True)
            return
        
        msg = '# Ideas\n\n'
        for i in data:
            self.logger.info(f'Adding idea from {i["user_id"]} to message')
            msg += f'## {i["type"]}\n\n'
            msg += f'**User:** {i["user_id"]}\n\n'
            msg += f'**Idea:** {i["idea"]}\n\n'
            
        with open('temp.md', 'w') as f:
            f.write(msg)
            
        await ctx.respond('Here you go:', file=discord.File('temp.md', filename='ideas.md'), ephemeral=True)
        os.remove('temp.md')
    

class MainIdeas(discord.ui.View):
    def __init__(self):
        self.logger = logging.getLogger('astolfo/Ideas/MainIdeas')
        super().__init__(timeout=None)
        self.logger.info('MainIdeas was initialized')
        
    
    @discord.ui.button(label='Submit an idea!', custom_id='submit_idea', style=discord.ButtonStyle.primary)
    async def submit_idea(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        self.logger.info('Submit an idea button pressed')
        await interaction.response.send_message('Select a category below and then fill out the form:', view=IdeasCategory(), ephemeral=True)
        self.stop()
        

class BotIdeaModal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(timeout=300, title='Submit a bot idea')
        self.logger = logging.getLogger('astolfo/Ideas/BotIdeaModal')
        self.logger.info('BotIdeaModal was initialized')
        self.add_item(InputText(label='Idea', placeholder='Enter your idea here', style=discord.InputTextStyle.paragraph))
        
    async def callback(self, interaction: discord.Interaction) -> None:
        self.logger.info('Callback was called')
        idea = self.children[0].value
        add_idea('bot', interaction.user.id, idea)
        await interaction.response.send_message('Idea was successfully submitted!', ephemeral=True)
        
    
class ServerIdeaModal(discord.ui.Modal):
    def __init__(self) -> None:
        self.logger = logging.getLogger('astolfo/Ideas/ServerIdeaModal')
        super().__init__(timeout=300, title='Submit a Discord server idea')
        
        self.add_item(InputText(label='Idea', placeholder='Enter your idea here', style=discord.InputTextStyle.paragraph))
        self.logger.info('ServerIdeaModal was initialized')
        
    async def callback(self, interaction: discord.Interaction) -> None:
        self.logger.info('Callback was called')
        idea = self.children[0].value
        add_idea('server', interaction.user.id, idea)
        await interaction.response.send_message('Idea was successfully submitted!', ephemeral=True)
        
        
class YouTubeIdeasModal(discord.ui.Modal):
    def __init__(self) -> None:
        self.logger = logging.getLogger('astolfo/Ideas/YouTubeIdeasModal')
        super().__init__(timeout=300, title='Submit a YouTube idea')
        
        self.add_item(InputText(label='Idea', placeholder='Enter your idea here', style=discord.InputTextStyle.paragraph))
        self.logger.info('YouTubeIdeasModal was initialized')
        
    async def callback(self, interaction: discord.Interaction) -> None:
        self.logger.info('Callback was called')
        idea = self.children[0].value
        add_idea('youtube', interaction.user.id, idea)
        await interaction.response.send_message('Idea was successfully submitted!', ephemeral=True)
        

class TikTokIdeasModal(discord.ui.Modal):
    def __init__(self) -> None:
        self.logger = logging.getLogger('astolfo/Ideas/TikTokIdeasModal')
        super().__init__(timeout=300, title='Submit a TikTok idea')
        
        self.add_item(InputText(label='Idea', placeholder='Enter your idea here', style=discord.InputTextStyle.paragraph))
        self.logger.info('TikTokIdeasModal was initialized')
        
    async def callback(self, interaction: discord.Interaction) -> None:
        self.logger.info('Callback was called')
        idea = self.children[0].value
        add_idea('tiktok', interaction.user.id, idea)
        await interaction.response.send_message('Idea was successfully submitted!', ephemeral=True)


class IdeasCategory(discord.ui.View):
    def __init__(self):
        self.logger = logging.getLogger('astolfo/Ideas/IdeasCategory')
        super().__init__(timeout=120)
        self.logger.info('IdeasCategory was initialized')
        
    
    @discord.ui.button(label='Bot idea', style=discord.ButtonStyle.primary)
    async def bot_idea(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        self.logger.info('Bot idea button pressed')
        await interaction.response.send_modal(BotIdeaModal())
        self.disable_all_items()
        self.stop()
    
    @discord.ui.button(label='Server idea', style=discord.ButtonStyle.primary)
    async def server_idea(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        self.logger.info('Server idea button pressed')
        await interaction.response.send_modal(ServerIdeaModal())
        self.disable_all_items()
        self.stop()
        
    @discord.ui.button(label='YouTube idea', style=discord.ButtonStyle.primary)
    async def youtube_idea(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        self.logger.info('YouTube idea button pressed')
        await interaction.response.send_modal(YouTubeIdeasModal())
        self.disable_all_items()
        self.stop()
        
    @discord.ui.button(label='TikTok idea', style=discord.ButtonStyle.primary)
    async def tiktok_idea(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        self.logger.info('TikTok idea button pressed')
        await interaction.response.send_modal(TikTokIdeasModal())
        self.disable_all_items()
        self.stop()
