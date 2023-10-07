import discord
import logging
import re
import constants

class BanInviteLinks(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo/BanInviteLinks')
        self.bot = bot
        super().__init__()
        self.logger.info('BanInviteLinks loaded')
        
    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.channel.id == constants.self_promo:
            self.logger.info('Ignoring message in self-promo channel')
            return
        
        match_1 = re.search(r'(https?:\/\/)?(www.)?(discord.(gg|io|me|li)|discordapp.com\/invite)\/[^\s\/]+', msg.content)
        if match_1 is not None:
            self.logger.info('Invite link detected')
            await msg.delete()
            await msg.channel.send(f'{msg.author.mention} Please do not send invite links to other servers here!', delete_after=5)
            return
