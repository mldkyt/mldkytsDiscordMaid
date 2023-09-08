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

