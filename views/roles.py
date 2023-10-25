import json

import discord
import discord.ui as ui
import constants


def has_nsfw_ban(target: discord.Member):
    with open('data/nsfw_bans.json') as f:
        data = json.load(f)

    return target.id in data


main_message = 'Welcome to the role selector! Select a category to begin!'


class MainView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.string_select(placeholder='Category', custom_id='roles_category', options=[
        discord.SelectOption(label='Pings', value='pings', description='Ping roles'),
        discord.SelectOption(label='Pronouns', value='pronouns',
                             description='Pronoun roles and trans role'),
        discord.SelectOption(label='Femboy Role', value='femboy', description='5 femboy stage roles'),
        discord.SelectOption(label='NSFW role', value='nsfw', description='NSFW role'),
        discord.SelectOption(label='Top or Bottom', value='topbottom', description='Top, Switch and Bottom roles')
    ], min_values=1, max_values=1)
    async def select(self, select: discord.ui.Select, interaction: discord.Interaction):
        if len(select.values) != 1:
            return

        if select.values[0] == 'pings':
            await interaction.response.send_message(content='Select ping roles below: ', view=PingRoleView(),
                                                    ephemeral=True)
        elif select.values[0] == 'pronouns':
            await interaction.response.send_message(content='Select pronoun roles below: ', view=PronounSelect(),
                                                    ephemeral=True)
        elif select.values[0] == 'femboy':
            await interaction.response.send_message(content='''Select a femboy stage below: 
- Stage 0: Access to femboy channels
- Stage 1: Acting feminine
- Stage 2: Shaving
- Stage 3: Thigh highs (Programming socks), Skirt, Crop top, ...
- Stage 4: Makeup
- Stage 5: TRAP >:3''', view=FemboyRoleSelectView(),
                                                    ephemeral=True)
        elif select.values[0] == 'nsfw':
            await interaction.response.send_message(content='Click below to get NSFW role: ', view=NsfwRoleSelectView(),
                                                    ephemeral=True)
        elif select.values[0] == 'topbottom':
            await interaction.response.send_message(content='Select top, switch and bottom roles: ',
                                                    view=TopBottomSelect(), ephemeral=True)
        else:
            await interaction.response.send_message(content='❌ Invalid selection', ephemeral=True)


class PingRoleView(ui.View):
    def __init__(self):
        super().__init__()

    @ui.button(label='New Video Pings', style=discord.ButtonStyle.blurple)
    async def toggle_new_vids(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        new_vids_role = guild.get_role(1133732578055168040)

        if new_vids_role not in interaction.user.roles:
            await interaction.user.add_roles(new_vids_role, reason='New videos role selected')
            await interaction.response.send_message('Added new videos role', ephemeral=True)
        else:
            await interaction.user.remove_roles(new_vids_role, reason='New videos role deselected')
            await interaction.response.send_message('Removed new videos role', ephemeral=True)

    @ui.button(label='Mod Update Pings', style=discord.ButtonStyle.blurple)
    async def toggle_game_mod_updates(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        game_mod_updates_role = guild.get_role(861679309394673696)

        if game_mod_updates_role not in interaction.user.roles:
            await interaction.user.add_roles(game_mod_updates_role, reason='Game mod updates role selected')
            await interaction.response.send_message('Added game mod updates role', ephemeral=True)
        else:
            await interaction.user.remove_roles(game_mod_updates_role, reason='Game mod updates role deselected')
            await interaction.response.send_message('Removed game mod updates role', ephemeral=True)

    @ui.button(label='Livestream Pings', style=discord.ButtonStyle.blurple)
    async def toggle_live_pings(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        live_pings_role = guild.get_role(1140290624654946445)

        if live_pings_role not in interaction.user.roles:
            await interaction.user.add_roles(live_pings_role, reason='Live pings role selected')
            await interaction.response.send_message('Added live pings role', ephemeral=True)
        else:
            await interaction.user.remove_roles(live_pings_role, reason='Live pings role deselected')
            await interaction.response.send_message('Removed live pings role', ephemeral=True)

    @ui.button(label='TikTok Pings', style=discord.ButtonStyle.blurple)
    async def toggle_tiktok_pings(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        tiktok_pings_role = guild.get_role(1152575554533478483)

        if tiktok_pings_role not in interaction.user.roles:
            await interaction.user.add_roles(tiktok_pings_role, reason='TikTok pings role selected')
            await interaction.response.send_message('Added TikTok pings role', ephemeral=True)
        else:
            await interaction.user.remove_roles(tiktok_pings_role, reason='TikTok pings role deselected')
            await interaction.response.send_message('Removed TikTok pings role', ephemeral=True)


class FemboyRoleSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(
            discord.ui.Button(label='Creator of these stages', url='https://www.youtube.com/watch?v=lPG-9fu7xLY',
                              row=2))

    @discord.ui.button(label='0', style=discord.ButtonStyle.blurple)
    async def stage_0_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild

        await interaction.response.defer(ephemeral=True, invisible=False)

        stage_0 = guild.get_role(constants.femboy_stage_0_role)
        stage_1 = guild.get_role(constants.femboy_stage_1_role)
        stage_2 = guild.get_role(constants.femboy_stage_2_role)
        stage_3 = guild.get_role(constants.femboy_stage_3_role)
        stage_4 = guild.get_role(constants.femboy_stage_4_role)
        stage_5 = guild.get_role(constants.femboy_stage_5_role)

        await interaction.user.add_roles(stage_0, reason='Stage 0 role selected')
        await interaction.user.remove_roles(stage_1, stage_2, stage_3, stage_4, stage_5, reason='Stage 0 role selected')
        await interaction.followup.send(content='Stage 0 femboy role selected')

    @discord.ui.button(label='1', style=discord.ButtonStyle.blurple)
    async def stage_1_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        await interaction.response.defer(ephemeral=True, invisible=False)
        stage_0 = guild.get_role(constants.femboy_stage_0_role)
        stage_1 = guild.get_role(constants.femboy_stage_1_role)
        stage_2 = guild.get_role(constants.femboy_stage_2_role)
        stage_3 = guild.get_role(constants.femboy_stage_3_role)
        stage_4 = guild.get_role(constants.femboy_stage_4_role)
        stage_5 = guild.get_role(constants.femboy_stage_5_role)

        await interaction.user.add_roles(stage_0, stage_1, reason='Stage 1 role selected')
        await interaction.user.remove_roles(stage_2, stage_3, stage_4, stage_5, reason='Stage 1 role selected')
        await interaction.followup.send(content='Stage 1 femboy role selected')

    @discord.ui.button(label='2', style=discord.ButtonStyle.blurple)
    async def stage_2_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        await interaction.response.defer(ephemeral=True, invisible=False)
        stage_0 = guild.get_role(constants.femboy_stage_0_role)
        stage_1 = guild.get_role(constants.femboy_stage_1_role)
        stage_2 = guild.get_role(constants.femboy_stage_2_role)
        stage_3 = guild.get_role(constants.femboy_stage_3_role)
        stage_4 = guild.get_role(constants.femboy_stage_4_role)
        stage_5 = guild.get_role(constants.femboy_stage_5_role)

        await interaction.user.add_roles(stage_0, stage_1, stage_2, reason='Stage 2 role selected')
        await interaction.user.remove_roles(stage_3, stage_4, stage_5, reason='Stage 2 role selected')
        await interaction.followup.send(content='Stage 2 femboy role selected')

    @discord.ui.button(label='3', style=discord.ButtonStyle.blurple)
    async def stage_3_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        await interaction.response.defer(ephemeral=True, invisible=False)
        stage_0 = guild.get_role(constants.femboy_stage_0_role)
        stage_1 = guild.get_role(constants.femboy_stage_1_role)
        stage_2 = guild.get_role(constants.femboy_stage_2_role)
        stage_3 = guild.get_role(constants.femboy_stage_3_role)
        stage_4 = guild.get_role(constants.femboy_stage_4_role)
        stage_5 = guild.get_role(constants.femboy_stage_5_role)

        await interaction.user.add_roles(stage_0, stage_1, stage_2, stage_3, reason='Stage 3 role selected')
        await interaction.user.remove_roles(stage_4, stage_5, reason='Stage 3 role selected')
        await interaction.followup.send(content='Stage 3 femboy role selected')

    @discord.ui.button(label='4', style=discord.ButtonStyle.blurple)
    async def stage_4_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        await interaction.response.defer(ephemeral=True, invisible=False)
        stage_0 = guild.get_role(constants.femboy_stage_0_role)
        stage_1 = guild.get_role(constants.femboy_stage_1_role)
        stage_2 = guild.get_role(constants.femboy_stage_2_role)
        stage_3 = guild.get_role(constants.femboy_stage_3_role)
        stage_4 = guild.get_role(constants.femboy_stage_4_role)
        stage_5 = guild.get_role(constants.femboy_stage_5_role)

        await interaction.user.add_roles(stage_0, stage_1, stage_2, stage_3, stage_4, reason='Stage 4 role selected')
        await interaction.user.remove_roles(stage_5, reason='Stage 4 role selected')
        await interaction.followup.send(content='Stage 4 femboy role selected')

    @discord.ui.button(label='5', style=discord.ButtonStyle.blurple)
    async def stage_5_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        await interaction.response.defer(ephemeral=True, invisible=False)
        stage_0 = guild.get_role(constants.femboy_stage_0_role)
        stage_1 = guild.get_role(constants.femboy_stage_1_role)
        stage_2 = guild.get_role(constants.femboy_stage_2_role)
        stage_3 = guild.get_role(constants.femboy_stage_3_role)
        stage_4 = guild.get_role(constants.femboy_stage_4_role)
        stage_5 = guild.get_role(constants.femboy_stage_5_role)

        await interaction.user.add_roles(stage_0, stage_1, stage_2, stage_3, stage_4, stage_5,
                                         reason='Stage 5 role selected')
        await interaction.followup.send(content='Stage 5 femboy role selected')

    @discord.ui.button(label='Remove', style=discord.ButtonStyle.red)
    async def remove_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        await interaction.response.defer(ephemeral=True, invisible=False)
        stage_0 = guild.get_role(constants.femboy_stage_0_role)
        stage_1 = guild.get_role(constants.femboy_stage_1_role)
        stage_2 = guild.get_role(constants.femboy_stage_2_role)
        stage_3 = guild.get_role(constants.femboy_stage_3_role)
        stage_4 = guild.get_role(constants.femboy_stage_4_role)
        stage_5 = guild.get_role(constants.femboy_stage_5_role)

        await interaction.user.remove_roles(stage_0, stage_1, stage_2, stage_3, stage_4, stage_5,
                                            reason='Deselected all stages')
        await interaction.followup.send(content='Removed all stages')


class NsfwRoleSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='NSFW role', style=discord.ButtonStyle.danger)
    async def toggle_nsfw_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        nsfw_role = guild.get_role(1152684011748077619)

        if nsfw_role not in interaction.user.roles:
            if has_nsfw_ban(interaction.user):
                await interaction.response.send_message('You are banned from the NSFW role', ephemeral=True)
                return
            await interaction.response.send_message('''# Hold on
With taking this role, you agree that you're 18+ and I'm not responsible if you get caught by your parents or something.
*Discard the message using the blue Discard button below the message.*''', view=NsfwRoleConfirmView(), ephemeral=True)
        else:
            await interaction.user.remove_roles(nsfw_role, reason='NSFW role deselected')
            await interaction.response.send_message('Removed NSFW role', ephemeral=True)


class NsfwRoleConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.danger)
    async def confirm_nsfw_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        nsfw_role = guild.get_role(1152684011748077619)

        if nsfw_role not in interaction.user.roles:
            if has_nsfw_ban(interaction.user):
                await interaction.response.send_message('You are banned from the NSFW role', ephemeral=True)
                return
            await interaction.user.add_roles(nsfw_role, reason='NSFW role selected')
            await interaction.response.send_message('Added NSFW role', ephemeral=True)
        else:
            await interaction.response.send_message('You already have the NSFW role', ephemeral=True)


# a member can have at most 1 role
class PronounSelect(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='he/him', style=discord.ButtonStyle.blurple)
    async def he_him(self, button: discord.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        role = guild.get_role(constants.he_him_role)
        if role not in member.roles:
            for i in constants.pronoun_roles:
                if i in [r.id for r in member.roles]:
                    await interaction.response.send_message('You can\'t have multiple pronoun roles', ephemeral=True)
                    return

            await member.add_roles(role, reason='he/him pronouns selected')
            await interaction.response.send_message('he/him pronouns added', ephemeral=True)
        else:
            await member.remove_roles(role, reason='he/him pronouns deselected')
            await interaction.response.send_message('he/him pronouns removed', ephemeral=True)

    @discord.ui.button(label='she/her', style=discord.ButtonStyle.blurple)
    async def she_her(self, button: discord.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        role = guild.get_role(constants.she_her_role)
        if role not in member.roles:
            for i in constants.pronoun_roles:
                if i in [r.id for r in member.roles]:
                    await interaction.response.send_message('You can\'t have multiple pronoun roles', ephemeral=True)
                    return

            await member.add_roles(role, reason='she/her pronouns selected')
            await interaction.response.send_message('she/her pronouns added', ephemeral=True)
        else:
            await member.remove_roles(role, reason='she/her pronouns deselected')
            await interaction.response.send_message('she/her pronouns removed', ephemeral=True)

    @discord.ui.button(label='they/them', style=discord.ButtonStyle.blurple)
    async def they_them(self, button: discord.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        role = guild.get_role(constants.they_them_role)
        if role not in member.roles:
            for i in constants.pronoun_roles:
                if i in [r.id for r in member.roles]:
                    await interaction.response.send_message('You can\'t have multiple pronoun roles', ephemeral=True)
                    return

            await member.add_roles(role, reason='they/them pronouns pronouns selected')
            await interaction.response.send_message('they/them pronouns pronouns added', ephemeral=True)
        else:
            await member.remove_roles(role, reason='they/them pronouns pronouns deselected')
            await interaction.response.send_message('they/them pronouns pronouns removed', ephemeral=True)

    @discord.ui.button(label='any pronouns', style=discord.ButtonStyle.blurple)
    async def any(self, button: discord.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        role = guild.get_role(constants.any_pronouns_role)
        if role not in member.roles:
            for i in constants.pronoun_roles:
                if i in [r.id for r in member.roles]:
                    await interaction.response.send_message('You can\'t have multiple pronoun roles', ephemeral=True)
                    return

            await member.add_roles(role, reason='Any pronouns pronouns selected')
            await interaction.response.send_message('Any pronouns pronouns added', ephemeral=True)
        else:
            await member.remove_roles(role, reason='Any pronouns pronouns deselected')
            await interaction.response.send_message('Any pronouns pronouns removed', ephemeral=True)

    @discord.ui.button(label='I am Trans', style=discord.ButtonStyle.blurple, row=2)
    async def trans(self, button: discord.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        role = guild.get_role(constants.trans_role)
        if role not in member.roles:
            await member.add_roles(role, reason='Trans role selected')
            await interaction.response.send_message('Trans role added', ephemeral=True)
        else:
            await member.remove_roles(role, reason='Trans role deselected')
            await interaction.response.send_message('Trans role removed', ephemeral=True)


class TopBottomSelect(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Top', style=discord.ButtonStyle.blurple)
    async def top(self, button: discord.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        role = guild.get_role(constants.top_role)
        if role not in member.roles:
            await member.add_roles(role, reason='Top role selected')
            await interaction.response.send_message('Top role added', ephemeral=True)
        else:
            await member.remove_roles(role, reason='Top role deselected')
            await interaction.response.send_message('Top role removed', ephemeral=True)

    @discord.ui.button(label='Bottom', style=discord.ButtonStyle.blurple)
    async def bottom(self, button: discord.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        role = guild.get_role(constants.bottom_role)
        if role not in member.roles:
            await member.add_roles(role, reason='Bottom role selected')
            await interaction.response.send_message('Bottom role added', ephemeral=True)
        else:
            await member.remove_roles(role, reason='Bottom role deselected')
            await interaction.response.send_message('Bottom role removed', ephemeral=True)

    @discord.ui.button(label='Switch', style=discord.ButtonStyle.blurple)
    async def switch(self, button: discord.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        role = guild.get_role(constants.switch_role)
        if role not in member.roles:
            await member.add_roles(role, reason='Switch role selected')
            await interaction.response.send_message('Switch role added', ephemeral=True)
        else:
            await member.remove_roles(role, reason='Switch role deselected')
            await interaction.response.send_message('Switch role removed', ephemeral=True)