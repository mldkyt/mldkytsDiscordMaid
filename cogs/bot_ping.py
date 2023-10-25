import logging
import discord

import constants

initial_message = '''# Hello there, %s!
I am a bot created by [Programmer Astolfo](https://github.com/ProgrammerAstolfo/ProgrammerAstolfoBot) to help with his server.
Use the buttons below to navigate through the pages.'''

chat_points_message = f'''# ChatPoints
ChatPoints are points given to everyone for chatting in the server.
You get 1 ChatPoint for every letter you send in a message.
You can check your balance with `/chatpoints` in <#{constants.commands_channel}>.'''

cute_points_message = f'''# CutePoints
CutePoints are points given to everyone who acts cute :3
You get 1 CatPoint for every cute thing you send in a message.
You can check your balance with `/cutepoints` in <#{constants.commands_channel}>.'''


class ChatPointsView(discord.ui.View):

    @discord.ui.button(label='Back to main page', style=discord.ButtonStyle.primary)
    async def chat_ponts(self, button: discord.ui.Button, interaction: discord.Interaction):
        logger = logging.getLogger('astolfo.BotPing.ChatPointsView')
        logger.info('Back to main page button pressed')
        await interaction.message.edit(content=(initial_message % interaction.user.mention), view=InitialView())
        await interaction.response.defer()


class CutePointsView(discord.ui.View):

    @discord.ui.button(label='Back to main page', style=discord.ButtonStyle.primary)
    async def chat_points(self, button: discord.ui.Button, interaction: discord.Interaction):
        logger = logging.getLogger('astolfo.BotPing.CutePointsView')
        logger.info('Back to main page button pressed')
        await interaction.message.edit(content=(initial_message % interaction.user.mention), view=InitialView())
        await interaction.response.defer()


class InitialView(discord.ui.View):

    @discord.ui.button(label='What are ChatPoints?', style=discord.ButtonStyle.primary)
    async def chat_ponts(self, button: discord.ui.Button, interaction: discord.Interaction):
        logger = logging.getLogger('astolfo.BotPing.InitialView')
        logger.info('What are ChatPoints button pressed')
        await interaction.message.edit(content=chat_points_message, view=ChatPointsView())
        await interaction.response.defer()

    @discord.ui.button(label='What are CutePoints?', style=discord.ButtonStyle.primary)
    async def cat_ponts(self, button: discord.ui.Button, interaction: discord.Interaction):
        logger = logging.getLogger('astolfo.BotPing/InitialView')
        logger.info('What are CutePoints button pressed')
        await interaction.message.edit(content=cute_points_message, view=CutePointsView())
        await interaction.response.defer()


class BotPing(discord.Cog):

    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo.BotPing')
        self.bot = bot
        super().__init__()
        self.logger.info('Initialization successful')

    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if f'<@{constants.bot_id}>' in msg.content:
            self.logger.info('Bot was pinged, sending message')
            await msg.channel.send(initial_message % msg.author.mention, view=InitialView())
