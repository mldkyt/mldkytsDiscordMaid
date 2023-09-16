import discord
import discord.ui as ui


class RoleSelectView(ui.View):
    @ui.button(label='New Video Pings', custom_id='new_video_pings', style=discord.ButtonStyle.blurple)
    async def toggle_new_vids(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        new_vids_role = guild.get_role(1133732578055168040)

        if new_vids_role not in interaction.user.roles:
            await interaction.user.add_roles(new_vids_role, reason='New videos role selected')
            await interaction.response.send_message('Added new videos role', ephemeral=True)
        else:
            await interaction.user.remove_roles(new_vids_role, reason='New videos role deselected')
            await interaction.response.send_message('Removed new videos role', ephemeral=True)

    @ui.button(label='Mod Update Pings', custom_id='game_mod_update_pings', style=discord.ButtonStyle.blurple)
    async def toggle_game_mod_updates(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        game_mod_updates_role = guild.get_role(861679309394673696)

        if game_mod_updates_role not in interaction.user.roles:
            await interaction.user.add_roles(game_mod_updates_role, reason='Game mod updates role selected')
            await interaction.response.send_message('Added game mod updates role', ephemeral=True)
        else:
            await interaction.user.remove_roles(game_mod_updates_role, reason='Game mod updates role deselected')
            await interaction.response.send_message('Removed game mod updates role', ephemeral=True)

    @ui.button(label='Livestream Pings', custom_id='livestream_pings', style=discord.ButtonStyle.blurple)
    async def toggle_live_pings(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        live_pings_role = guild.get_role(1140290624654946445)

        if live_pings_role not in interaction.user.roles:
            await interaction.user.add_roles(live_pings_role, reason='Live pings role selected')
            await interaction.response.send_message('Added live pings role', ephemeral=True)
        else:
            await interaction.user.remove_roles(live_pings_role, reason='Live pings role deselected')
            await interaction.response.send_message('Removed live pings role', ephemeral=True)

    @ui.button(label='TikTok Pings', custom_id='tiktok_pings', style=discord.ButtonStyle.blurple)
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
    @discord.ui.button(label='Femboy', custom_id='role_femboy', style=discord.ButtonStyle.blurple)
    async def toggle_femboy_pings(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        femboy_pings_role = guild.get_role(1152575598439444580)

        if femboy_pings_role not in interaction.user.roles:
            await interaction.user.add_roles(femboy_pings_role, reason='Femboy role selected')
            await interaction.response.send_message('Added femboy role', ephemeral=True)
        else:
            await interaction.user.remove_roles(femboy_pings_role, reason='Femboy role deselected')
            await interaction.response.send_message('Removed femboy role', ephemeral=True)


class NsfwRoleSelectView(discord.ui.View):
    @discord.ui.button(label='NSFW role', custom_id='role_nsfw', style=discord.ButtonStyle.danger)
    async def toggle_nsfw_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        nsfw_role = guild.get_role(1152684011748077619)

        if nsfw_role not in interaction.user.roles:
            await interaction.response.send_message('''# Hold on
With taking this role, you agree that you're 18+ and if you are under 18, you will be banned if we find out.''', view=NsfwRoleConfirmView(timeout=10), ephemeral=True)
        else:
            await interaction.user.remove_roles(nsfw_role, reason='NSFW role deselected')
            await interaction.response.send_message('Removed NSFW role', ephemeral=True)


class NsfwRoleConfirmView(discord.ui.View):
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.danger)
    async def confirm_nsfw_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        nsfw_role = guild.get_role(1152684011748077619)

        if nsfw_role not in interaction.user.roles:
            await interaction.user.add_roles(nsfw_role, reason='NSFW role selected')
            await interaction.response.send_message('Added NSFW role', ephemeral=True)
        
        await interaction.message.delete()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.blurple)
    async def cancel_nsfw_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
