
import json
import logging
import discord
from discord.interactions import Interaction
from discord.ui.input_text import InputText
import constants
import os

from utils.language import get_string, get_user_lang

def init():
    if not os.path.exists('data/reports.json'):
        with open('data/reports.json', 'w') as f:
            json.dump([], f, indent=4)


def add_report(member: discord.Member, type: str, message: str):
    with open('data/reports.json', 'r+') as f:
        reports: list = json.load(f)
        
    reports.append({
        'id': member.id,
        'name': member.name,
        'message': message,
        'type': type
    })
    
    with open('data/reports.json', 'w') as f:
        json.dump(reports, f, indent=4)
        

class ReportCommand(discord.Cog):
    
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.ReportCommand')
        self.bot = bot
        init()
        super().__init__()
        self.logger.info('ReportCommand initialization successful')
        
    @discord.slash_command(guild_ids=[constants.guild_id])
    @discord.option(name='type', choices=['dm spam', 'bad language', 'bad images', 'bad word(s) in bio', 'rule violation', 'filter bypass', 'weird behaviour', 'way too silly :3'])
    async def report(self, ctx: discord.ApplicationContext, member: discord.Member, type: str):
        lang = get_user_lang(ctx.author.id)
        if member.bot:
            await ctx.respond(get_string('report_error_bot', lang), ephemeral=True)
            return
        if constants.moderator_role in [r.id for r in member.roles]:
            await ctx.respond(get_string('report_error_mod', lang), ephemeral=True)
            return
        if member.id == ctx.author.id:
            await ctx.respond(get_string('report_error_self', lang), ephemeral=True)
            return
        
        modal = ReportModal(member, type)
        await ctx.response.send_modal(modal)
        
        
class ReportModal(discord.ui.Modal):
    def __init__(self, member: discord.Member, type: str) -> None:
        self.member = member
        self.type = type
        
        lang = get_user_lang(member.id)
        super().__init__(title=get_string('report_modal_title', lang) % self.member.display_name, timeout=1200)
        
        self.add_item(
            discord.ui.InputText(label='Message', style=discord.InputTextStyle.long)
        )
        
    async def callback(self, interaction: Interaction):
        message = self.children[0].value
        add_report(self.member, self.type, message)
        self.stop()
        lang = get_user_lang(self.member.id)
        await interaction.response.send_message(get_string('report_success', lang) % (self.member.display_name), ephemeral=True)