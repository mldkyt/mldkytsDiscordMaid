import discord

import views.roles


class DevCommands(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        super().__init__()

    @discord.slash_command()
    @discord.option(name='template', description='The template to send', type=discord.SlashCommandOptionType.string, required=True, choices=[
        "roles_pings",
        "roles_femboy",
        "roles_nsfw"
    ])
    async def send_template_msg(self, ctx: discord.ApplicationContext, template: str):
        if ctx.user.id != 575536897141637120 and ctx.user.id != 1149748649446883358:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if template == 'roles_pings':
            await ctx.channel.send('''# Ping Roles
Select the roles you want to be pinged for below. You can select multiple roles.''', view=views.roles.RoleSelectView(timeout=None))
            await ctx.respond('Send the message successfully', ephemeral=True)
        elif template == 'roles_femboy':
            await ctx.channel.send('''# The one and only FEMBOY role
Selecting this role will hoist you and make you a femboy ❤️❤️''', view=views.roles.FemboyRoleSelectView(timeout=None))
            await ctx.respond('Send the message successfully', ephemeral=True)
        elif template == 'roles_nsfw':
            await ctx.channel.send('''# NSFW role
Selecting this role will give you access to NSFW channels, you have to be 18+ to select this role.''', view=views.roles.NsfwRoleSelectView(timeout=None))
        else:
            await ctx.respond('Invalid template', ephemeral=True)
