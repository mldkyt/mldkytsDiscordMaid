
import logging
import discord
from discord.ui.item import Item
import constants


slash_command_message = '# Welcome to the server!\nPlease verify yourself by clicking the button below.'
verify_0 = '''# (0/4) Welcome to %s
You are going to pick roles and then you\'ll get verified.
Click Next to continue'''
verify_1 = '''# (1/4)Please pick your **preferred** pronoun role'''
verify_2 = '''# (2/4)Please pick your femboy stage, or skip this question
- 0: Access to femboy channels
- 1: Acting feminine
- 2: Shaving
- 3: Thigh highs (Programming socks), skirt, Crop top, ...
- 4: Makeup
- 5: TRAP >:3'''
verify_3 = '''# (3/4)Please pick your top/bottom/switch role or skip this question'''
verify_4 = '''# Thank you for selection your roles!
Click finish to get verified!'''

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
            interaction.guild.get_role(constants.verified_role)        
        ]
        resetting = False
        for role in roles:
            if role in interaction.user.roles:
                if not resetting:
                    await interaction.response.defer(invisible=False, ephemeral=True)
                resetting = True
                await interaction.user.remove_roles(role)
                
        if resetting:
            await interaction.followup.send(verify_0 % interaction.guild.name, view=VerifyStart())
        else:
            await interaction.response.send_message(verify_0 % interaction.guild.name, view=VerifyStart(), ephemeral=True)
        
    
class VerifyStart(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        
    @discord.ui.button(label='Next', style=discord.ButtonStyle.green)
    async def verify_next(self, button: discord.ui.Button, interaction: discord.Interaction):        
        await interaction.response.edit_message(content=verify_1, view=VerifyPronouns())
        
class VerifyPronouns(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        
    @discord.ui.button(label='He/Him', style=discord.ButtonStyle.green)
    async def verify_he_him(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=verify_2, view=VerifyFemboy())
        
        he_him_role = interaction.guild.get_role(constants.he_him_role)
        await interaction.user.add_roles(he_him_role)
        
    @discord.ui.button(label='She/Her', style=discord.ButtonStyle.green)
    async def verify_she_her(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=verify_2, view=VerifyFemboy())
        
        she_her_role = interaction.guild.get_role(constants.she_her_role)
        await interaction.user.add_roles(she_her_role)
        
    @discord.ui.button(label='They/Them', style=discord.ButtonStyle.green)
    async def verify_they_them(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=verify_2, view=VerifyFemboy())
        
        they_them_role = interaction.guild.get_role(constants.they_them_role)
        await interaction.user.add_roles(they_them_role)
        
    @discord.ui.button(label='Any pronouns', style=discord.ButtonStyle.green)
    async def verify_any_pronouns(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=verify_2, view=VerifyFemboy())
        
        any_pronouns_role = interaction.guild.get_role(constants.any_pronouns_role)
        await interaction.user.add_roles(any_pronouns_role)
        

class VerifyFemboy(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        
    @discord.ui.button(label='0')
    async def verify_stage_0(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=verify_3, view=VerifyTopBottom())
        
        stage_0 = interaction.guild.get_role(constants.femboy_stage_0_role)
        await interaction.user.add_roles(stage_0)
        
    @discord.ui.button(label='1')
    async def verify_stage_1(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=verify_3, view=VerifyTopBottom())
        
        stage_0 = interaction.guild.get_role(constants.femboy_stage_0_role)
        await interaction.user.add_roles(stage_0)
        stage_1 = interaction.guild.get_role(constants.femboy_stage_1_role)
        await interaction.user.add_roles(stage_1)
        
    @discord.ui.button(label='2')
    async def verify_stage_2(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=verify_3, view=VerifyTopBottom())
        
        stage_0 = interaction.guild.get_role(constants.femboy_stage_0_role)
        await interaction.user.add_roles(stage_0)
        stage_1 = interaction.guild.get_role(constants.femboy_stage_1_role)
        await interaction.user.add_roles(stage_1)
        stage_2 = interaction.guild.get_role(constants.femboy_stage_2_role)
        await interaction.user.add_roles(stage_2)
        
    @discord.ui.button(label='3')
    async def verify_stage_3(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=verify_3, view=VerifyTopBottom())
        
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
        await interaction.response.edit_message(content=verify_3, view=VerifyTopBottom())
        
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
        await interaction.response.edit_message(content=verify_3, view=VerifyTopBottom())
        
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
        
    @discord.ui.button(label='I am not a femboy', style=discord.ButtonStyle.danger)
    async def verify_skip_femboy(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(verify_3, view=VerifyTopBottom())
    
        
class VerifyTopBottom(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label='Top')
    async def verify_top(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=verify_4, view=VerifyFinish())
        
        top_role = interaction.guild.get_role(constants.top_role)
        await interaction.user.add_roles(top_role)
        
    @discord.ui.button(label='Bottom')
    async def verify_bottom(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=verify_4, view=VerifyFinish())
        
        bottom_role = interaction.guild.get_role(constants.bottom_role)
        await interaction.user.add_roles(bottom_role)
        
    @discord.ui.button(label='Switch')
    async def verify_switch(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=verify_4, view=VerifyFinish())
        
        switch_role = interaction.guild.get_role(constants.switch_role)
        await interaction.user.add_roles(switch_role)
        
    @discord.ui.button(label='I don\'t want to/Skip', style=discord.ButtonStyle.danger)
    async def verify_skip_top_bottom(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=verify_4, view=VerifyFinish())
    
class VerifyFinish(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label='Finish', style=discord.ButtonStyle.green)
    async def verify_finish(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        
        verified_role = interaction.guild.get_role(constants.verified_role)
        await interaction.user.add_roles(verified_role)
        