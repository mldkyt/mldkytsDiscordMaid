
import json
import os
import discord
from discord.ui.input_text import InputText
from discord.ui.item import Item

def init():
    if not os.path.exists('data/analytics_from.json'):
        with open('data/analytics_from.json', 'w') as f:
            json.dump([], f)

def add_vote(user: int, vote: str):
    with open('data/analytics_from.json') as f:
        data: list = json.load(f)
        
    for i in data:
        if i['user'] == user:
            i['from'] = vote
            break
    else:
        data.append({
            'user': user,
            'from': vote
        })
        
    with open('data/analytics_from.json', 'w') as f:
        json.dump(data, f)
        
def add_vote_custom(user: int, vote: str, message: str):
    with open('data/analytics_from.json') as f:
        data: list = json.load(f)
        
    for i in data:
        if i['user'] == user:
            i['from'] = vote
            i['message'] = message
            break
    else:
        data.append({
            'user': user,
            'from': vote,
            'message': message
        })
    
    with open('data/analytics_from.json', 'w') as f:
        json.dump(data, f)
        
def has_user_voted(user: int):
    with open('data/analytics_from.json') as f:
        data: list = json.load(f)
        
    return any(i['user'] == user for i in data)


class AnalyticsFrom(discord.ui.View):
    """Where you came from."""
    def __init__(self):
        init()
        super().__init__(timeout=None)
        
    @discord.ui.button(label='I came from TikTok', custom_id='analytics:from:tiktok', style=discord.ButtonStyle.blurple)
    async def from_tiktok(self, button: discord.ui.Button, interaction: discord.Interaction):
        if has_user_voted(interaction.user.id):
            await interaction.response.send_message('You already voted!', ephemeral=True)
            return
        
        add_vote(interaction.user.id, 'tiktok')
        await interaction.response.send_message('Your feedback was submitted successfully', ephemeral=True)
    
    @discord.ui.button(label='I came from YouTube', custom_id='analytics:from:youtube', style=discord.ButtonStyle.blurple)
    async def from_youtube(self, button: discord.ui.Button, interaction: discord.Interaction):
        if has_user_voted(interaction.user.id):
            await interaction.response.send_message('You already voted!', ephemeral=True)
            return
        
        add_vote(interaction.user.id, 'youtube')
        await interaction.response.send_message('Your feedback was submitted successfully', ephemeral=True)
        
    @discord.ui.button(label='A friend invited me', custom_id='analytics:from:friend', style=discord.ButtonStyle.secondary)
    async def from_friend(self, button: discord.ui.Button, interaction: discord.Interaction):
        if has_user_voted(interaction.user.id):
            await interaction.response.send_message('You already voted!', ephemeral=True)
            return
        
        add_vote(interaction.user.id, 'friend')
        await interaction.response.send_message('Your feedback was submitted successfully', ephemeral=True)
        
    @discord.ui.button(label='Custom response...', custom_id='analytics:from:custom', style=discord.ButtonStyle.gray)
    async def from_custom(self, button: discord.ui.Button, interaction: discord.Interaction):
        if has_user_voted(interaction.user.id):
            await interaction.response.send_message('You already voted!', ephemeral=True)
            return
        
        await interaction.response.send_modal(AnalyticsFromCustom())

class AnalyticsFromCustom(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title='Custom feedback', custom_id='analytics:from:custom', timeout=240)
        
        self.children.append(
            discord.ui.InputText(
                placeholder='I came from...',
                label='Where did you come from?',
                min_length=5,
                required=True,
                style=discord.InputTextStyle.paragraph
            )
        )
        
    async def callback(self, interaction: discord.Interaction):
        if has_user_voted(interaction.user.id):
            await interaction.response.send_message('You already voted!', ephemeral=True)
            return
        
        add_vote_custom(interaction.user.id, 'custom', self.children[0].value)
        await interaction.response.send_message('Your feedback was submitted successfully', ephemeral=True)