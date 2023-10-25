
import logging

import discord

import constants


class OwoChannelLimit(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.OwoChannelLimit')
        self.bot = bot
        if constants.owo_uwu_channel == 0:
            self.logger.warning('Owo channel limit is disabled because channel is not specified')
            return
        super().__init__()
        self.logger.info('OwO channel limit initialization successful')
        
    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.channel.id != constants.owo_uwu_channel:
            return
        if msg.content.lower() != 'owo' and msg.content.lower() != 'uwu':
            await msg.delete()
            await msg.channel.send(f'{msg.author.mention} This channel is only for OwO and UwU, nothing else~ :3', delete_after=5)
            
    @discord.Cog.listener()
    async def on_message_edit(self, old: discord.Message, new: discord.Message):
        if new.author.bot:
            return
        if new.channel.id != constants.owo_uwu_channel:
            return
        if new.content.lower() != 'owo' and new.content.lower() != 'uwu':
            await new.delete()
            await new.channel.send(f'{new.author.mention} This channel is only for OwO and UwU, nothing else~ :3', delete_after=5)
