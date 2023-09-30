import discord

import constants

initial_message = '''# Hello there, %s!
I am a bot created by [Astolph0](https://github.com/ProgrammerAstolfo/ProgrammerAstolfoBot) to help with his server.
Use the buttons below to navigate through the pages.'''

chat_points_message = f'''# ChatPoints
ChatPoints are points given to everyone for chatting in the server.
You get 1 ChatPoint for every letter you send in a message.
You can check your balance with `/chatpoints` in <#{constants.commands_channel}>.'''

cat_points_message = f'''# CatPoints
CatPoints are points given to everyone when they use :3 in a message.
You get 1 CatPoint for every :3 (and some variations of it) you send in a message.
You can check your balance with `/catpoints` in <#{constants.commands_channel}>.'''


class ChatPointsView(discord.ui.View):

    @discord.ui.button(label='Back to main page', style=discord.ButtonStyle.primary)
    async def chat_ponts(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.edit(content=(initial_message % interaction.user.mention), view=InitialView())
        await interaction.response.defer()


class CatPointsView(discord.ui.View):

    @discord.ui.button(label='Back to main page', style=discord.ButtonStyle.primary)
    async def chat_ponts(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.edit(content=(initial_message % interaction.user.mention), view=InitialView())
        await interaction.response.defer()


class InitialView(discord.ui.View):

    @discord.ui.button(label='What are ChatPoints?', style=discord.ButtonStyle.primary)
    async def chat_ponts(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.edit(content=chat_points_message, view=ChatPointsView())
        await interaction.response.defer()

    @discord.ui.button(label='What are CatPoints?', style=discord.ButtonStyle.primary)
    async def cat_ponts(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.edit(content=cat_points_message, view=CatPointsView())
        await interaction.response.defer()


class BotPing(discord.Cog):

    def __init__(self, bot: discord.Bot):
        self.bot = bot
        super().__init__()

    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if f'<@{constants.bot_id}>' in msg.content:
            await msg.channel.send(initial_message % msg.author.mention, view=InitialView())
