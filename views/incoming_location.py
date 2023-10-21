import json
import os

import discord.ui
from discord import Interaction


def init():
    if not os.path.exists('data/analytics_incoming.json'):
        with open('data/analytics_incoming.json', 'w') as f:
            json.dump({}, f)


def has_selected_incoming(member: int) -> bool:
    with open('data/analytics_incoming.json', 'r') as f:
        data = json.load(f)

    if str(member) in data:
        return True
    return False


def set_selected_incoming(member: int, selected: str):
    with open('data/analytics_incoming.json', 'r') as f:
        data = json.load(f)

    if str(member) in data:
        return

    data[str(member)] = selected

    with open('data/analytics_incoming.json', 'w') as f:
        json.dump(data, f)


class IncomingLocationModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(timeout=None, title='Incoming Location')
        self.add_item(discord.ui.InputText(label='Where did you come from', placeholder='I came from...',
                                           style=discord.InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        set_selected_incoming(interaction.user.id, 'CUSTOM:' + self.children[0].value)
        await interaction.response.send_message('Thank you for your feedback', ephemeral=True)


class IncomingLocation(discord.ui.View):
    def __init__(self):
        init()
        super().__init__(timeout=None)

    @discord.ui.button(label='I came from TikTok', custom_id='incoming_tiktok', style=discord.ButtonStyle.primary)
    async def came_from_tiktok(self, button: discord.ui.Button, ctx: discord.Interaction):
        if has_selected_incoming(ctx.user.id):
            await ctx.response.send_message('You already selected!', ephemeral=True)
            return

        set_selected_incoming(ctx.user.id, 'tiktok')
        await ctx.response.send_message('Thank you for the feedback', ephemeral=True)

    @discord.ui.button(label='I came from YouTube', custom_id='incoming_youtube', style=discord.ButtonStyle.primary)
    async def came_from_youtube(self, button: discord.ui.Button, ctx: discord.Interaction):
        if has_selected_incoming(ctx.user.id):
            await ctx.response.send_message('You already selected!', ephemeral=True)
            return

        set_selected_incoming(ctx.user.id, 'youtube')
        await ctx.response.send_message('Thank you for the feedback', ephemeral=True)

    @discord.ui.button(label='My friend invited me', custom_id='incoming_friend', style=discord.ButtonStyle.primary)
    async def came_from_friend(self, button: discord.ui.Button, ctx: discord.Interaction):
        if has_selected_incoming(ctx.user.id):
            await ctx.response.send_message('You already selected!', ephemeral=True)
            return

        set_selected_incoming(ctx.user.id, 'friend invitation')
        await ctx.response.send_message('Thank you for the feedback', ephemeral=True)

    @discord.ui.button(label='Other', custom_id='incoming_other', style=discord.ButtonStyle.primary)
    async def came_from_other(self, button: discord.ui.Button, ctx: discord.Interaction):
        modal = IncomingLocationModal()
        await ctx.response.send_modal(modal)
