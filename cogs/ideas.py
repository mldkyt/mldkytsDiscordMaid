import json
import logging
import discord
from discord.ui.input_text import InputText
from discord.ui.item import Item
import os
import constants
from utils.language import get_string, get_user_lang

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
        self.logger = logging.getLogger('astolfo.Ideas')
        self.bot = bot
        init()
        super().__init__()

    
temp_lang = 'en'

class MainIdeas(discord.ui.View):
    def __init__(self):
        self.logger = logging.getLogger('astolfo.Ideas.MainIdeas')
        super().__init__(timeout=None)

        
    
    @discord.ui.button(label='Submit an idea!', custom_id='submit_idea', style=discord.ButtonStyle.primary)
    async def submit_idea(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:

        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.send_message(get_string('ideas_select_category', lang), view=IdeasCategory(), ephemeral=True)
        

class IdeaSubmissionModal(discord.ui.Modal):
    def __init__(self, user: discord.Member, modal_type: str) -> None:
        lang = get_user_lang(user.id)
        super().__init__(timeout=300, title=get_string('ideas_category_%s_title' % (modal_type), lang))
        self.logger = logging.getLogger('astolfo.Ideas.BotIdeaModal')
        self.add_item(InputText(
            label=get_string('ideas_idea_label', lang),
            placeholder=get_string('ideas_idea_placeholder', lang), 
            style=discord.InputTextStyle.paragraph
            ))

        self.modal_type = modal_type
        
    async def callback(self, interaction: discord.Interaction) -> None:

        idea = self.children[0].value
        add_idea(self.modal_type, interaction.user.id, idea)
        await interaction.response.send_message('Idea was successfully submitted!', ephemeral=True)


class IdeasCategory(discord.ui.View):
    def __init__(self):
        self.logger = logging.getLogger('astolfo.Ideas.IdeasCategory')
        super().__init__(timeout=120)

    
    @discord.ui.button(label=get_string('ideas_category_bot', temp_lang), style=discord.ButtonStyle.primary)
    async def bot_idea(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:

        await interaction.response.send_modal(IdeaSubmissionModal(interaction.user, 'bot'))
    
    @discord.ui.button(label=get_string('ideas_category_server', temp_lang), style=discord.ButtonStyle.primary)
    async def server_idea(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:

        await interaction.response.send_modal(IdeaSubmissionModal(interaction.user, 'server'))
        
    @discord.ui.button(label=get_string('ideas_category_youtube', temp_lang), style=discord.ButtonStyle.primary)
    async def youtube_idea(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:

        await interaction.response.send_modal(IdeaSubmissionModal(interaction.user, 'youtube'))
        
    @discord.ui.button(label=get_string('ideas_category_tiktok', temp_lang), style=discord.ButtonStyle.primary)
    async def tiktok_idea(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:

        await interaction.response.send_modal(IdeaSubmissionModal(interaction.user, 'tiktok'))
