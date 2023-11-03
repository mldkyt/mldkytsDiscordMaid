import discord

import cogs.ideas
import constants
from views.roles import MainView
from views.analytics_from import AnalyticsFrom


class DevCommands(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        super().__init__()

    @discord.slash_command(guild_ids=[constants.guild_id])
    @discord.option(name='template', description='The template to send', type=discord.SlashCommandOptionType.string,
                    required=True,
                    choices=["roles", 'ideas', 'analytics-from'])
    async def send_template_msg(self, ctx: discord.ApplicationContext, template: str):
        if ctx.user.id != 575536897141637120 and ctx.user.id != 1149748649446883358:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if template == 'roles':
            await ctx.respond('Send message successfully', ephemeral=True)
            await ctx.channel.send(content='# The role selector\nStart below: ', view=MainView())
        elif template == 'ideas':
            await ctx.channel.send('''# Ideas
Submit ideas by clicking the button below :3''', view=cogs.ideas.MainIdeas())
            await ctx.respond('Send the message successfully', ephemeral=True)
        elif template == 'analytics-from':
            await ctx.channel.send('''# For analytical purposes: Where did you come from?
||@everyone||''', view=AnalyticsFrom())
            await ctx.respond('Send the message successfully', ephemeral=True)
        else:
            await ctx.respond('Invalid template', ephemeral=True)
