import logging

import discord

import constants


class FemboyMediaHearting(discord.Cog):
    def __init__(self):
        self.logger = logging.getLogger('astolfo.FemboyMediaHearting')
        super().__init__()


    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.channel.id == constants.femboy_media_channel:

            await msg.add_reaction('❤️')
