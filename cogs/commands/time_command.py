
import datetime
import logging
import discord
import constants
from utils.language import get_user_lang, get_string

class TimeCommand(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.TimeCommand')
        self.bot = bot
        super().__init__()
        self.logger.info('Initialization successful')

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def time(self, ctx: discord.ApplicationContext):
        self.logger.info('Getting time and sending to message')
        utc_time = datetime.datetime.now()
        mldkyt_time = utc_time + datetime.timedelta(hours=2)
        lang = get_user_lang(ctx.author.id)
        await ctx.respond(get_string('time', lang) % (
            utc_time.strftime("%H:%M"), 
            utc_time.strftime("%I:%M %p"), 
            mldkyt_time.strftime("%H:%M"), 
            mldkyt_time.strftime("%I:%M %p")
            ))
