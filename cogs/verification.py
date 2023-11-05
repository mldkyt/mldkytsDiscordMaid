
import logging
import discord
from discord.ui.item import Item
import constants
from utils.language import get_string, get_user_lang


slash_command_message = '# Welcome to the server!\nPlease verify yourself by clicking the button below.'
temp_lang = 'en'

class Verification(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.Verification')
        self.bot = bot
        super().__init__()
        self.logger.info('Loaded cog Verification')

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def send_verification_message(self, ctx: discord.ApplicationContext):
        if ctx.user.id != constants.bot_maintainer:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        await ctx.channel.send(slash_command_message, view=VerifyMain())
        await ctx.respond('Sending verification message', ephemeral=True)

    @discord.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        verify_channel = self.bot.get_channel(constants.verify_channel)
        msg = await verify_channel.send(f'{member.mention}, please verify here')
        await msg.delete()


class VerifyMain(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Verify', style=discord.ButtonStyle.green, custom_id='verify')
    async def start_verification(self, button: discord.ui.Button, interaction: discord.Interaction):
        roles = [
            interaction.guild.get_role(constants.he_him_role),
            interaction.guild.get_role(constants.she_her_role),
            interaction.guild.get_role(constants.they_them_role),
            interaction.guild.get_role(constants.any_pronouns_role),
            interaction.guild.get_role(constants.femboy_stage_0_role),
            interaction.guild.get_role(constants.femboy_stage_1_role),
            interaction.guild.get_role(constants.femboy_stage_2_role),
            interaction.guild.get_role(constants.femboy_stage_3_role),
            interaction.guild.get_role(constants.femboy_stage_4_role),
            interaction.guild.get_role(constants.femboy_stage_5_role),
            interaction.guild.get_role(constants.top_role),
            interaction.guild.get_role(constants.bottom_role),
            interaction.guild.get_role(constants.switch_role),
            interaction.guild.get_role(constants.verified_role),
            interaction.guild.get_role(1133732578055168040),
            interaction.guild.get_role(1140290624654946445),
            interaction.guild.get_role(1152575554533478483)
        ]
        resetting = False
        for role in roles:
            if role in interaction.user.roles:
                if not resetting:
                    await interaction.response.defer(invisible=False, ephemeral=True)
                resetting = True
                await interaction.user.remove_roles(role)

        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        if resetting:
            await interaction.followup.send(get_string('verify_1', lang) % interaction.guild.name, view=VerifyStart())
        else:
            await interaction.response.send_message(get_string('verify_1', lang) % interaction.guild.name, view=VerifyStart(), ephemeral=True)


class VerifyStart(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label=get_string('verify_1_next', temp_lang), style=discord.ButtonStyle.green)
    async def verify_next(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_2', lang), view=VerifyPronouns())


class VerifyPronouns(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label=get_string('verify_2_he/him', temp_lang), style=discord.ButtonStyle.green)
    async def verify_he_him(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_3', lang), view=VerifyFemboy())

        he_him_role = interaction.guild.get_role(constants.he_him_role)
        await interaction.user.add_roles(he_him_role)

    @discord.ui.button(label=get_string('verify_2_she/her', temp_lang), style=discord.ButtonStyle.green)
    async def verify_she_her(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_3', lang), view=VerifyFemboy())

        she_her_role = interaction.guild.get_role(constants.she_her_role)
        await interaction.user.add_roles(she_her_role)

    @discord.ui.button(label=get_string('verify_2_they/them', temp_lang), style=discord.ButtonStyle.green)
    async def verify_they_them(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_3', lang), view=VerifyFemboy())

        they_them_role = interaction.guild.get_role(constants.they_them_role)
        await interaction.user.add_roles(they_them_role)

    @discord.ui.button(label=get_string('verify_2_any', temp_lang), style=discord.ButtonStyle.green)
    async def verify_any_pronouns(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_3', lang), view=VerifyFemboy())

        any_pronouns_role = interaction.guild.get_role(
            constants.any_pronouns_role)
        await interaction.user.add_roles(any_pronouns_role)


class VerifyFemboy(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label='0')
    async def verify_stage_0(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_4', lang), view=VerifyPings())

        stage_0 = interaction.guild.get_role(constants.femboy_stage_0_role)
        await interaction.user.add_roles(stage_0)

    @discord.ui.button(label='1')
    async def verify_stage_1(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_4', lang), view=VerifyPings())

        stage_0 = interaction.guild.get_role(constants.femboy_stage_0_role)
        await interaction.user.add_roles(stage_0)
        stage_1 = interaction.guild.get_role(constants.femboy_stage_1_role)
        await interaction.user.add_roles(stage_1)

    @discord.ui.button(label='2')
    async def verify_stage_2(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_4', lang), view=VerifyPings())

        stage_0 = interaction.guild.get_role(constants.femboy_stage_0_role)
        await interaction.user.add_roles(stage_0)
        stage_1 = interaction.guild.get_role(constants.femboy_stage_1_role)
        await interaction.user.add_roles(stage_1)
        stage_2 = interaction.guild.get_role(constants.femboy_stage_2_role)
        await interaction.user.add_roles(stage_2)

    @discord.ui.button(label='3')
    async def verify_stage_3(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_4', lang), view=VerifyPings())

        stage_0 = interaction.guild.get_role(constants.femboy_stage_0_role)
        await interaction.user.add_roles(stage_0)
        stage_1 = interaction.guild.get_role(constants.femboy_stage_1_role)
        await interaction.user.add_roles(stage_1)
        stage_2 = interaction.guild.get_role(constants.femboy_stage_2_role)
        await interaction.user.add_roles(stage_2)
        stage_3 = interaction.guild.get_role(constants.femboy_stage_3_role)
        await interaction.user.add_roles(stage_3)

    @discord.ui.button(label='4')
    async def verify_stage_4(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_4', lang), view=VerifyPings())

        stage_0 = interaction.guild.get_role(constants.femboy_stage_0_role)
        await interaction.user.add_roles(stage_0)
        stage_1 = interaction.guild.get_role(constants.femboy_stage_1_role)
        await interaction.user.add_roles(stage_1)
        stage_2 = interaction.guild.get_role(constants.femboy_stage_2_role)
        await interaction.user.add_roles(stage_2)
        stage_3 = interaction.guild.get_role(constants.femboy_stage_3_role)
        await interaction.user.add_roles(stage_3)
        stage_4 = interaction.guild.get_role(constants.femboy_stage_4_role)
        await interaction.user.add_roles(stage_4)

    @discord.ui.button(label='5')
    async def verify_stage_5(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_4', lang), view=VerifyPings())

        stage_0 = interaction.guild.get_role(constants.femboy_stage_0_role)
        await interaction.user.add_roles(stage_0)
        stage_1 = interaction.guild.get_role(constants.femboy_stage_1_role)
        await interaction.user.add_roles(stage_1)
        stage_2 = interaction.guild.get_role(constants.femboy_stage_2_role)
        await interaction.user.add_roles(stage_2)
        stage_3 = interaction.guild.get_role(constants.femboy_stage_3_role)
        await interaction.user.add_roles(stage_3)
        stage_4 = interaction.guild.get_role(constants.femboy_stage_4_role)
        await interaction.user.add_roles(stage_4)
        stage_5 = interaction.guild.get_role(constants.femboy_stage_5_role)
        await interaction.user.add_roles(stage_5)

    @discord.ui.button(label=get_string('verify_3_not_a_femboy', temp_lang), style=discord.ButtonStyle.danger)
    async def verify_skip_femboy(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_4', lang), view=VerifyPings())


class VerifyPings(discord.ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(label='New Video Pings')
    async def verify_new_video_pings(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        new_video_pings_role = interaction.guild.get_role(constants.new_videos_role)
        if new_video_pings_role in interaction.user.roles:
            await interaction.user.remove_roles(new_video_pings_role)
            await interaction.response.edit_message(content=get_string('verify_4', lang), view=VerifyPings())
        else:
            await interaction.user.add_roles(new_video_pings_role)
            await interaction.response.edit_message(content=get_string('verify_4', lang), view=VerifyPings())
            
    @discord.ui.button(label='New Stream Pings')
    async def verify_new_stream_pings(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        new_stream_pings_role = interaction.guild.get_role(constants.live_pings_role)
        if new_stream_pings_role in interaction.user.roles:
            await interaction.user.remove_roles(new_stream_pings_role)
            await interaction.response.edit_message(content=get_string('verify_4', lang), view=VerifyPings())
        else:
            await interaction.user.add_roles(new_stream_pings_role)
            await interaction.response.edit_message(content=get_string('verify_4', lang), view=VerifyPings())
            
    @discord.ui.button(label='New TikTok Pings')
    async def verify_new_tiktok_pings(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        tiktok_pings_role = interaction.guild.get_role(constants.tiktok_pings_role)
        if tiktok_pings_role in interaction.user.roles:
            await interaction.user.remove_roles(tiktok_pings_role)
            await interaction.response.edit_message(content=get_string('verify_4', lang), view=VerifyPings())
        else:
            await interaction.user.add_roles(tiktok_pings_role)
            await interaction.response.edit_message(content=get_string('verify_4', lang), view=VerifyPings())
            
    @discord.ui.button(label='Next')
    async def verify_next(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_5', lang), view=VerifyTopBottom())


class VerifyTopBottom(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Top')
    async def verify_top(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_6', lang), view=VerifyFinish())

        top_role = interaction.guild.get_role(constants.top_role)
        await interaction.user.add_roles(top_role)

    @discord.ui.button(label='Bottom')
    async def verify_bottom(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_6', lang), view=VerifyFinish())

        bottom_role = interaction.guild.get_role(constants.bottom_role)
        await interaction.user.add_roles(bottom_role)

    @discord.ui.button(label='Switch')
    async def verify_switch(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_6', lang), view=VerifyFinish())

        switch_role = interaction.guild.get_role(constants.switch_role)
        await interaction.user.add_roles(switch_role)

    @discord.ui.button(label=get_string('verify_5_skip', temp_lang), style=discord.ButtonStyle.danger)
    async def verify_skip_top_bottom(self, button: discord.ui.Button, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user.id)
        global temp_lang
        temp_lang = lang
        await interaction.response.edit_message(content=get_string('verify_6', lang), view=VerifyFinish())


class VerifyFinish(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label=get_string('verify_6_finish', temp_lang), style=discord.ButtonStyle.green)
    async def verify_finish(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.disable_all_items()
        await interaction.response.edit_message(view=self)

        verified_role = interaction.guild.get_role(constants.verified_role)
        await interaction.user.add_roles(verified_role)
