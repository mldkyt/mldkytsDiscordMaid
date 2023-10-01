import json
import discord

import views.roles
import cogs.ideas
import constants

def cleanup_data(user: int):
    with open('data/catpoints.json') as f:
        catpoints = json.load(f)
    # list of {user_id: str, catpoints: int}

    for i in range(len(catpoints)):
        if catpoints[i]['user_id'] == user:
            catpoints.pop(i)
            break

    with open('data/catpoints.json', 'w') as f:
        json.dump(catpoints, f, indent=4)

    with open('data/chatpoints.json') as f:
        chatpoints = json.load(f)
    # list of {user_id: str, catpoints: int}

    for i in range(len(chatpoints)):
        if chatpoints[i]['user_id'] == user:
            chatpoints.pop(i)
            break

    with open('data/chatpoints.json', 'w') as f:
        json.dump(chatpoints, f, indent=4)

    with open('data/dailymsg.json') as f:
        dailymsg = json.load(f)
    # list of {user_id: str, catpoints: int}

    for i in range(len(dailymsg)):
        if dailymsg[i]['user_id'] == user:
            dailymsg.pop(i)
            break

    with open('data/dailymsg.json', 'w') as f:
        json.dump(dailymsg, f, indent=4)

    with open('data/yearlymsg.json') as f:
        yearlymsg = json.load(f)
    # list of {user_id: str, catpoints: int}

    for i in range(len(yearlymsg)):
        if yearlymsg[i]['user_id'] == user:
            yearlymsg.pop(i)
            break

    with open('data/yearlymsg.json', 'w') as f:
        json.dump(yearlymsg, f, indent=4)


class DevCommands(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        super().__init__()

    @discord.slash_command(guild_ids=[constants.guild_id])
    @discord.option(name='template', description='The template to send', type=discord.SlashCommandOptionType.string, required=True, choices=[
        "roles_pings",
        "roles_femboy",
        "roles_nsfw",
        "roles_pronouns",
        "roles_trans",
        "roles_topbottom",
        'ideas'
    ])
    async def send_template_msg(self, ctx: discord.ApplicationContext, template: str):
        if ctx.user.id != 575536897141637120 and ctx.user.id != 1149748649446883358:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if template == 'roles_pings':
            await ctx.channel.send('''# Ping Roles
Select the roles you want to be pinged for below. You can select multiple roles.''', view=views.roles.RoleSelectView())
            await ctx.respond('Send the message successfully', ephemeral=True)
        elif template == 'roles_femboy':
            await ctx.channel.send('''# Femboy
Select a femboy stage according to the info below:
**Stage 0:** You are not a femboy, but love femboys. (Gives access to femboy channels)
**Stage 1:** Acting feminine
**Stage 2:** Shaving yourself
**Stage 3:** Feminine clothing
**Stage 4:** Make-up
**Stage 5:** YOU'RE A MF TRAP
**PWETTY PWEASE SELECT THESE ACCORDING TO REALITY AND DON'T SELECT STAGE 4 JUST BECAUSE IT PUTS YOU ON THE TOP I BEG YOU!**''', view=views.roles.FemboyRoleSelectView())
            await ctx.respond('Send the message successfully', ephemeral=True)
        elif template == 'roles_nsfw':
            await ctx.channel.send('''# NSFW role
Selecting this role will give you access to NSFW channels, you have to be 18+ to select this role.
Not being old enough will get you banned from taking the role.''', view=views.roles.NsfwRoleSelectView())
            await ctx.respond('Send the message successfully', ephemeral=True)
        elif template == 'roles_pronouns':
            await ctx.channel.send('''# Pronoun roles
Select 1 pronoun role below''', view=views.roles.PronounSelect())
            await ctx.respond('Send the message successfully', ephemeral=True)
        elif template == 'roles_trans':
            await ctx.channel.send('''# Trans role
If you\'re trans, select it here :3''', view=views.roles.TransSelect())
            await ctx.respond('Send the message successfully', ephemeral=True)
        elif template == 'roles_topbottom':
            await ctx.channel.send('''# Top/Switch/Bottom role
Select your Top/Switch/Bottom role here :3''', view=views.roles.TopBottomSelect())
            await ctx.respond('Send the message successfully', ephemeral=True)
        elif template == 'ideas':
            await ctx.channel.send('''# Ideas
Submit ideas by clicking the button below :3''', view=cogs.ideas.MainIdeas())
            await ctx.respond('Send the message successfully', ephemeral=True)
        else:
            await ctx.respond('Invalid template', ephemeral=True)
            
    @discord.slash_command(guild_ids=[constants.guild_id])
    async def test_delete_user(self, ctx: discord.ApplicationContext, user: str):
        if ctx.user.id != constants.bot_maintainer:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return
        
        cleanup_data(int(user))
        await ctx.respond('Deleted user data', ephemeral=True)

    
    @discord.slash_command(guild_ids=[constants.guild_id])
    async def send_message_as_bot(self, ctx: discord.ApplicationContext, content: str):
        if ctx.user.id != constants.bot_maintainer:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return
        
        await ctx.channel.send(content)
        await ctx.respond('Message was sent as bot.', ephemeral=True)
