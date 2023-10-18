import logging

import discord

import constants


class FemboyMediaHearting(discord.Cog):
    def __init__(self):
        self.logger = logging.getLogger('astolfo.FemboyMediaHearting')
        super().__init__()
        self.logger.info('Initialization successful')

    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.channel.id == constants.femboy_media_channel:
            self.logger.info(f'Message from {msg.author} sent in {msg.channel.mention}')
            await msg.add_reaction('❤️')
