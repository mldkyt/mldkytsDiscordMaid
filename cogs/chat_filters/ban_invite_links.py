import discord
import logging
import re
import constants
from utils.language import get_string, get_user_lang

class BanInviteLinks(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.BanInviteLinks')
        self.bot = bot
        super().__init__()

        
    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.channel.id == constants.self_promo:

            return
        
        match_1 = re.search(r'(https?://)?(www.)?(discord.(gg|io|me|li)|discordapp.com/invite)/[^\s/]+', msg.content)
        if match_1 is not None:

            await msg.delete()
            lang = get_user_lang(msg.author.id)
            await msg.channel.send(get_string('invite_links_banned', lang) % (msg.author.mention), delete_after=5)
            return
