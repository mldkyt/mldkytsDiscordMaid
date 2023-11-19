
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


    @discord.slash_command(guild_ids=[constants.guild_id])
    async def time(self, ctx: discord.ApplicationContext):

        utc_time = datetime.datetime.now()
        programmer_astolfo_time = utc_time + datetime.timedelta(hours=2)
        lang = get_user_lang(ctx.author.id)
        await ctx.respond(get_string('time', lang) % (
            utc_time.strftime("%H:%M"), 
            utc_time.strftime("%I:%M %p"), 
            programmer_astolfo_time.strftime("%H:%M"), 
            programmer_astolfo_time.strftime("%I:%M %p")
            ))
