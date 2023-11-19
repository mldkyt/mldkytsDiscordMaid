import os

import logging

import discord
import sentry_sdk
from discord import Color, Embed
from discord.ext.commands import CommandOnCooldown
from cogs.femboy_of_the_month import FemboyOfTheMonth

import constants
from cogs.bot_ping import BotPing
from cogs.points.cute_points import CutePoints
from cogs.points.chat_points import ChatPoints
from cogs.message_counters.daily_messages import DailyMessages
from cogs.commands.dev_commands import DevCommands
from cogs.event_logger import EventLogger
from cogs.commands.moderation_commands import ModerationCommands
from cogs.status import Status
from cogs.commands.time_command import TimeCommand
from cogs.unixsocks import UnixSocks
from cogs.website_sync import WebsiteSync
from cogs.message_counters.yearly_messages import YearlyMessages
from cogs.channel_specific.bot_commands_reminder import BotCommandsReminder
from cogs.ideas import Ideas, MainIdeas
from cogs.linux_uptime import Uptime
from cogs.welcome_goodbye import WelcomeGoodbye
from cogs.ghost_pings import GhostPings
from cogs.channel_specific.nya_channel_limit import NyaChannelLimit
from cogs.chat_filters.ban_invite_links import BanInviteLinks
from views.analytics_from import AnalyticsFrom
from cogs.channel_specific.column_3_channel import Column3Chat
from cogs.channel_specific.owo_channel_limit import OwoChannelLimit
from cogs.message_reactions import MessageReactions
from cogs.commands.report_command import ReportCommand
from cogs.testing import Testing
from cogs.verification import Verification, VerifyMain
from cogs.channel_specific.daily_fun_fact_limit import DailyFunFactLimit
from cogs.commands.language_commands import LanguageCommands
from views.roles import MainView
from cogs.commands.brimo_command import BrimoCommand

sentry_sdk.init(
    dsn=constants.sentry_url,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0
)

# add file handler
logger = logging.getLogger()
file_handler = logging.FileHandler('logs.log', 'a', 'utf8', delay=True)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(name)s :: %(message)s', datefmt='%d/%m/%Y %H:%M:%S'))
logger.addHandler(file_handler)

main_logger = logging.getLogger('astolfo.__main__')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = discord.Bot(intents=intents)

if not os.path.exists('data'):
    os.mkdir('data')

bot.add_cog(Status(bot))
bot.add_cog(DailyMessages(bot))
bot.add_cog(YearlyMessages(bot))
bot.add_cog(BotPing(bot))
bot.add_cog(CutePoints(bot))
bot.add_cog(ChatPoints(bot))
bot.add_cog(ModerationCommands(bot))
bot.add_cog(WebsiteSync(bot))
bot.add_cog(DevCommands(bot))
bot.add_cog(EventLogger(bot))
bot.add_cog(UnixSocks(bot))
bot.add_cog(TimeCommand(bot))
bot.add_cog(BotCommandsReminder(bot))
bot.add_cog(Ideas(bot))
bot.add_cog(Uptime(bot))
bot.add_cog(WelcomeGoodbye(bot))
bot.add_cog(GhostPings(bot))
bot.add_cog(NyaChannelLimit(bot))
bot.add_cog(BanInviteLinks(bot))
bot.add_cog(Column3Chat(bot))
bot.add_cog(OwoChannelLimit(bot))
bot.add_cog(MessageReactions(bot))
bot.add_cog(ReportCommand(bot))

if constants.dev_mode:
    bot.add_cog(Testing())

bot.add_cog(Verification(bot))
bot.add_cog(DailyFunFactLimit(bot))
bot.add_cog(FemboyOfTheMonth(bot))
bot.add_cog(LanguageCommands(bot))
bot.add_cog(BrimoCommand(bot))

@bot.event
async def on_ready():

    bot.add_view(MainView())
    bot.add_view(MainIdeas())
    bot.add_view(VerifyMain())
    bot.add_view(AnalyticsFrom())

# Handle slash command errors, if it's a cooldown error, send a message to the user
@bot.event
async def on_slash_command_error(ctx: discord.ApplicationContext, error):
    if isinstance(error, CommandOnCooldown):
        embed = Embed(title='You are on cooldown cutie :3',
                      description=f'Try again in about {int(round(error.retry_after, 0))} seconds :3',
                      color=Color.red())
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        raise error

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
        embed = Embed(title='You are on cooldown cutie :3',
                      description=f'Try again in about {int(round(error.retry_after, 0))} seconds :3',
                      color=Color.red())
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        raise error


@bot.slash_command(guild_ids=[constants.guild_id])
async def changelog(ctx: discord.ApplicationContext):
    with open('changelog.md') as f:
        await ctx.respond(f.read())


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
    await ctx.respond("Here you go: ", file=discord.File('temp.md', filename='changelog.md'))
    os.remove('temp.md')


bot.run(constants.token)
