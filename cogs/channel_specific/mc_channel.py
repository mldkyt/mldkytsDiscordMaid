import logging

import discord
import requests
from discord.ext import tasks

import constants

server_offline_msg = '''# Minecraft Server
Status: **Offline**
IP: **Not available** at this moment
Minecraft Version: 1.20.1'''

server_online_msg = '''# Minecraft Server
Status: Online
IP: **%s**
Minecraft Version: 1.20.1'''


class MCChannel(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo/MCChannel')
        if constants.ngrok_token == '' or constants.mc_channel_id == 0 or constants.mc_message_id == 0:
            self.logger.warning('Skipping Minecraft channel checker because parameters are not defined')
            return
        self.bot = bot
        self.last_status = 'offline'
        self.last_msg = ''
        super().__init__()
        self.logger.info('Minecraft Channel module initiated')

    @discord.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(constants.mc_channel_id)
        message = await channel.fetch_message(constants.mc_message_id)
        self.last_msg = message.content
        self.update_mc_server.start()

    async def update_message(self):
        self.logger.info('Updating message')
        ngrok_data = requests.get('https://api.ngrok.com/tunnels', headers={
            'Ngrok-Version': '2',
            'Authorization': f'Bearer {constants.ngrok_token}'
        }).json()

        for i in ngrok_data['tunnels']:
            if i['forwards_to'] == 'localhost:25565':
                final_msg = server_online_msg % (i['public_url'][6:])
                break
        else:
            final_msg = server_offline_msg

        if self.last_msg == final_msg:
            return

        self.last_msg = final_msg
        channel = self.bot.get_channel(constants.mc_channel_id)
        message = await channel.fetch_message(constants.mc_message_id)
        await message.edit(content=final_msg)

    @tasks.loop(hours=1)
    async def update_mc_server(self):
        await self.update_message()

    @discord.slash_command()
    async def mc_server_manual_refresh(self, ctx: discord.ApplicationContext):
        if ctx.user.id != constants.bot_maintainer:
            await ctx.respond('Not permission', ephemeral=True)
            return

        await self.update_message()
        await ctx.respond('Updated.', ephemeral=True)
