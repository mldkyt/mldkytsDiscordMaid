import os

import discord
from discord import Color, Embed
from discord.ext.commands import CommandOnCooldown

import constants
from cogs.auto_goodmorning_goodnight import AutoGoodMorningGoodNight
from cogs.bot_ping import BotPing
from cogs.cat_points import CatPoints
from cogs.chat_points import ChatPoints
from cogs.daily_messages import DailyMessages
from cogs.dev_commands import DevCommands
from cogs.event_logger import EventLogger
from cogs.moderation_commands import ModerationCommands
from cogs.status import Status
from cogs.time_command import TimeCommand
from cogs.unixsocks import UnixSocks
from cogs.website_sync import WebsiteSync
from cogs.yearly_messages import YearlyMessages
from cogs.bot_commands_reminder import BotCommandsReminder
from cogs.ideas import Ideas, MainIdeas
from views.roles import FemboyRoleSelectView, NsfwRoleSelectView, PronounSelect, RoleSelectView, TopBottomSelect, TransSelect

bot = discord.Bot(intents=discord.Intents.default() | discord.Intents.message_content | discord.Intents.members | discord.Intents.presences)

bot.add_cog(Status(bot))
bot.add_cog(DailyMessages(bot))
bot.add_cog(YearlyMessages(bot))
bot.add_cog(BotPing(bot))
bot.add_cog(CatPoints(bot))
bot.add_cog(ChatPoints(bot))
bot.add_cog(ModerationCommands(bot))
bot.add_cog(WebsiteSync(bot))
bot.add_cog(DevCommands(bot))
bot.add_cog(AutoGoodMorningGoodNight(bot))
bot.add_cog(EventLogger(bot))
bot.add_cog(UnixSocks(bot))
bot.add_cog(TimeCommand(bot))
bot.add_cog(BotCommandsReminder(bot))
bot.add_cog(Ideas(bot))

@bot.event
async def on_ready():
    print('Ready!')
    bot.add_view(RoleSelectView())
    bot.add_view(FemboyRoleSelectView())
    bot.add_view(NsfwRoleSelectView())
    bot.add_view(PronounSelect())
    bot.add_view(TransSelect())
    bot.add_view(TopBottomSelect())
    bot.add_view(MainIdeas())


@bot.slash_command(guild_ids=[constants.guild_id])
async def version(ctx: discord.ApplicationContext):
    # base the update date from the modification date of the bot's folder
    with open('changelog.md') as f:
        data = f.read()

    data = data.split('\n')[0]
    await ctx.respond(f'mld\'s bot {data[2:].lower()} running on GNU/Linux', ephemeral=True)


@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error):
    if isinstance(error, CommandOnCooldown):
        embed = Embed(title='You are on cooldown cutie :3', description=f'Try again in about {int(round(error.retry_after, 0))} seconds :3', color=Color.red())
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        raise error


@bot.slash_command(guild_ids=[constants.guild_id])
async def changelog(ctx: discord.ApplicationContext):
    with open('changelog.md') as f:
        await ctx.respond(f.read(), ephemeral=True)


@bot.slash_command(guild_ids=[constants.guild_id])
async def full_changelog(ctx: discord.ApplicationContext):
    """Attaches the full changelog."""
    with open('changelog.md') as f:
        data_1 = f.read()
    with open('changelog_old.md') as f:
        data_2 = f.read()

    data = data_1 + data_2
    with open('temp.md', 'w') as f:
        f.write(data)
    await ctx.respond("Here you go: ", file=discord.File('temp.md', filename='changelog.md'), ephemeral=True)
    os.remove('temp.md')


bot.run(constants.token)
