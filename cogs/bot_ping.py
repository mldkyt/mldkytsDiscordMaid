import logging
import discord

import constants
from utils.language import get_string, get_user_lang


class ChatPointsView(discord.ui.View):

    @discord.ui.button(label='Back to main page', style=discord.ButtonStyle.primary)
    async def chat_ponts(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        await interaction.message.edit(content=(get_string('bot_mention', lang) % interaction.user.mention), view=InitialView())
        await interaction.response.defer()


class CutePointsView(discord.ui.View):

    @discord.ui.button(label='Back to main page', style=discord.ButtonStyle.primary)
    async def chat_points(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        await interaction.message.edit(content=(get_string('bot_mention', lang) % interaction.user.mention), view=InitialView())
        await interaction.response.defer()


class InitialView(discord.ui.View):

    @discord.ui.button(label='What are ChatPoints?', style=discord.ButtonStyle.primary)
    async def chat_ponts(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        await interaction.message.edit(content=get_string('bot_mention_chatpoints', lang), view=ChatPointsView())
        await interaction.response.defer()

    @discord.ui.button(label='What are CutePoints?', style=discord.ButtonStyle.primary)
    async def cat_ponts(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        await interaction.message.edit(content=get_string('bot_mention_cutepoints', lang), view=CutePointsView())
        await interaction.response.defer()


class BotPing(discord.Cog):

    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo.BotPing')
        self.bot = bot
        super().__init__()


    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if f'<@{constants.bot_id}>' in msg.content:

            lang = get_user_lang(msg.author.id)
            await msg.channel.send(get_string('bot_mention', lang) % msg.author.mention, view=InitialView())
