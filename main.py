from pathlib import Path

import discord

import constants
from cogs.auto_answer import AutoAnswer
from cogs.bot_ping import BotPing
from cogs.cat_points import CatPoints
from cogs.chat_points import ChatPoints
from cogs.daily_messages import DailyMessages
from cogs.moderation_commands import ModerationCommands
from cogs.status import Status
from cogs.website_sync import WebsiteSync
from cogs.welcome_goodbye import WelcomeGoodbye
from cogs.yearly_messages import YearlyMessages
from views.roles import RoleSelectView

bot = discord.Bot(intents=discord.Intents.default() | discord.Intents.message_content | discord.Intents.members | discord.Intents.presences)

bot.add_cog(AutoAnswer(bot))
bot.add_cog(WelcomeGoodbye(bot))
bot.add_cog(Status(bot))
bot.add_cog(DailyMessages(bot))
bot.add_cog(YearlyMessages(bot))
bot.add_cog(BotPing(bot))
bot.add_cog(CatPoints(bot))
bot.add_cog(ChatPoints(bot))
bot.add_cog(ModerationCommands(bot))
bot.add_cog(WebsiteSync(bot))


@bot.event
async def on_ready():
    print('Ready!')
    bot.add_view(RoleSelectView(timeout=None))


@bot.slash_command(guild_ids=[constants.guild_id])
async def send_roles_msg(ctx: discord.ApplicationContext):
    if ctx.user.id != constants.bot_maintainer:
        return await ctx.respond('You are not allowed to use this command!', ephemeral=True)
    await ctx.channel.send('# Ping Roles\nThese roles will let you get pinged', view=RoleSelectView())
    await ctx.respond('Sent roles message!', ephemeral=True)


@bot.slash_command(guild_ids=[constants.guild_id])
async def version(ctx: discord.ApplicationContext):
    # base the update date from the modification date of the bot's folder
    await ctx.respond(f'**Version:** 1.0.0', ephemeral=True)


bot.run(constants.token)
