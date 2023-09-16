from pathlib import Path

import discord

import constants
from cogs.auto_answer import AutoAnswer
from cogs.bot_ping import BotPing
from cogs.cat_points import CatPoints
from cogs.chat_points import ChatPoints
from cogs.daily_messages import DailyMessages
from cogs.dev_commands import DevCommands
from cogs.moderation_commands import ModerationCommands
from cogs.status import Status
from cogs.website_sync import WebsiteSync
from cogs.welcome_goodbye import WelcomeGoodbye
from cogs.yearly_messages import YearlyMessages
from views.roles import FemboyRoleSelectView, NsfwRoleSelectView, RoleSelectView

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
bot.add_cog(DevCommands(bot))


@bot.event
async def on_ready():
    print('Ready!')
    bot.add_view(RoleSelectView(timeout=None))
    bot.add_view(FemboyRoleSelectView(timeout=None))
    bot.add_view(NsfwRoleSelectView(timeout=None))


@bot.slash_command(guild_ids=[constants.guild_id])
async def version(ctx: discord.ApplicationContext):
    # base the update date from the modification date of the bot's folder
    await ctx.respond(f'**Version:** 1.2.0 - Added NSFW role into role selection', ephemeral=True)


bot.run(constants.token)
