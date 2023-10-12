import os

import logging
import threading

import discord
from discord import Color, Embed
from discord.ext.commands import CommandOnCooldown

import asyncio
import constants
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
from cogs.linux_uptime import Uptime
from cogs.welcome_goodbye import WelcomeGoodbye
from cogs.ghost_pings import GhostPings
from cogs.nya_channel_limit import NyaChannelLimit
from cogs.ban_invite_links import BanInviteLinks
from website.main import run_app
from cogs.column_3_channel import Column3Chat
from cogs.owo_channel_limit import OwoChannelLimit
from cogs.message_reactions import MessageReactions
from cogs.report_command import ReportCommand
from views.roles import FemboyRoleSelectView, NsfwRoleSelectView, PronounSelect, RoleSelectView, TopBottomSelect, \
    TransSelect

logging.basicConfig(level=logging.INFO)
# add file handler
logger = logging.getLogger()
handler = logging.FileHandler(filename='logs.log', encoding='utf-8')
# print to console
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s'))

main_logger = logging.getLogger('astolfo')

bot = discord.Bot(
    intents=discord.Intents.default() | discord.Intents.message_content | discord.Intents.members | discord.Intents.presences)

main_logger.info('Starting website')
web_thread = threading.Thread(target=lambda: run_app(bot), name='astolfo/Website')
web_thread.daemon = True
web_thread.start()

main_logger.info('Loading module: Status')
bot.add_cog(Status(bot))
main_logger.info('Loading module: Daily Messages')
bot.add_cog(DailyMessages(bot))
main_logger.info('Loading module: Yearly messages')
bot.add_cog(YearlyMessages(bot))
main_logger.info('Loading module: Bot ping')
bot.add_cog(BotPing(bot))
main_logger.info('Loading module: CatPoints')
bot.add_cog(CatPoints(bot))
main_logger.info('Loading module: ChatPoints')
bot.add_cog(ChatPoints(bot))
main_logger.info('Loading module: Moderation Commands')
bot.add_cog(ModerationCommands(bot))
main_logger.info('Loading module: Website Synchronization')
bot.add_cog(WebsiteSync(bot))
main_logger.info('Loading module: Developer Commands')
bot.add_cog(DevCommands(bot))
main_logger.info('Loading module: Event Logger')
bot.add_cog(EventLogger(bot))
main_logger.info('Loading module: r/UnixSocks')
bot.add_cog(UnixSocks(bot))
main_logger.info('Loading module: Time')
bot.add_cog(TimeCommand(bot))
main_logger.info('Loading module: Bot Commands Reminder')
bot.add_cog(BotCommandsReminder(bot))
main_logger.info('Loading module: Ideas')
bot.add_cog(Ideas(bot))
main_logger.info('Loading module: Uptime')
bot.add_cog(Uptime(bot))
main_logger.info('Loading module: Welcome & Goodbye')
bot.add_cog(WelcomeGoodbye(bot))
main_logger.info('Loading module: Ghost pings')
bot.add_cog(GhostPings(bot))
main_logger.info('Loading module: Nya channel limit')
bot.add_cog(NyaChannelLimit(bot))
main_logger.info('Loading module: Ban invite links')
bot.add_cog(BanInviteLinks(bot))
main_logger.info('Loading module: :3 channel limit')
bot.add_cog(Column3Chat(bot))
main_logger.info('Loading module: OwO channel limit')
bot.add_cog(OwoChannelLimit(bot))
main_logger.info('Loading module: Message reactions')
bot.add_cog(MessageReactions(bot))
main_logger.info('Loading module: Report Command')
bot.add_cog(ReportCommand(bot))


@bot.event
async def on_ready():
    main_logger.info('Logged in and ready to go!')
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
        embed = Embed(title='You are on cooldown cutie :3',
                      description=f'Try again in about {int(round(error.retry_after, 0))} seconds :3',
                      color=Color.red())
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
