import asyncio
import datetime
import json
import logging

import discord

import constants


# warnings are an array of {userid: str, reason: str, moderator: str}


def init():
    try:
        with open('data/warnings.json'):
            pass
    except FileNotFoundError:
        with open('data/warnings.json', 'w') as f:
            f.write('[]')

    try:
        with open('data/nsfw_bans.json'):
            pass
    except FileNotFoundError:
        with open('data/nsfw_bans.json', 'w') as f:
            f.write('[]')


def add_warning(user: discord.Member, reason: str, moderator: discord.Member):
    with open('data/warnings.json') as f:
        warnings: list = json.load(f)
    warnings.append({'userid': user.id, 'reason': reason,
                     'moderator': moderator.id})
    with open('data/warnings.json', 'w') as f:
        json.dump(warnings, f)


def get_warnings(user: discord.Member):
    with open('data/warnings.json') as f:
        warnings: list = json.load(f)
    return [warning for warning in warnings if warning['userid'] == user.id]


def add_nsfw_ban(user: discord.Member):
    with open('data/nsfw_bans.json') as f:
        bans: list = json.load(f)

    if user.id not in bans:
        bans.append(user.id)

    with open('data/nsfw_bans.json', 'w') as f:
        json.dump(bans, f)


def remove_nsfw_ban(user: discord.Member):
    with open('data/nsfw_bans.json') as f:
        bans: list = json.load(f)

    if user.id in bans:
        bans.remove(user.id)

    with open('data/nsfw_bans.json', 'w') as f:
        json.dump(bans, f)
        

def add_chatpoints(user: int, chatpoints: int):
    with open('data/chatpoints.json') as f:
        data: list = json.load(f)
        
    for user_data in data:
        if user_data['user_id'] == user:
            if 'chatpoints' not in user_data:
                user_data['chatpoints'] = 0
            user_data['chatpoints'] += chatpoints
            break
    else:
        data.append({'user_id': user, 'chatpoints': chatpoints})
        
    with open('data/chatpoints.json', 'w') as f:
        json.dump(data, f)
        
def remove_chatpoints(user: int, chatpoints: int):
    with open('data/chatpoints.json') as f:
        data: list = json.load(f)
        
    for user_data in data:
        if user_data['user_id'] == user:
            if 'chatpoints' not in user_data:
                user_data['chatpoints'] = 0
            user_data['chatpoints'] -= chatpoints
            break
    else:
        data.append({'user_id': user, 'chatpoints': chatpoints})
        
    with open('data/chatpoints.json', 'w') as f:
        json.dump(data, f)
        
def add_cutepoints(user: int, cutepoints: int):
    with open('data/cutepoints.json') as f:
        data: list = json.load(f)
        
    for user_data in data:
        if user_data['user_id'] == user:
            if 'cutepoints' not in user_data:
                user_data['cutepoints'] = 0
            user_data['cutepoints'] += cutepoints
            break
    else:
        data.append({'user_id': user, 'cutepoints': cutepoints})
    
    with open('data/cutepoints.json', 'w') as f:
        json.dump(data, f)
        
def remove_cutepoints(user: int, cutepoints: int):
    with open('data/cutepoints.json') as f:
        data: list = json.load(f)
        
    for user_data in data:
        if user_data['user_id'] == user:
            if 'cutepoints' not in user_data:
                user_data['cutepoints'] = 0
            user_data['cutepoints'] -= cutepoints
            break
    else:
        data.append({'user_id': user, 'cutepoints': cutepoints})
        
    with open('data/cutepoints.json', 'w') as f:
        json.dump(data, f)


class ModerationCommands(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo.ModerationCommands')
        self.bot = bot
        init()
        super().__init__()
        self.logger.info('Initialization successful')
        
    mod_group = discord.SlashCommandGroup('moderation', description='Moderation commands', guild_ids=[constants.guild_id])
    admin_group = discord.SlashCommandGroup('admin', description='Admin commands', guild_ids=[constants.guild_id])

    @mod_group.slash_command(guild_ids=[constants.guild_id])
    async def clear(self, ctx: discord.ApplicationContext, search_past: int,
                    author: discord.Member = None, not_author: discord.Member = None,
                    starts_with: str = None, ends_with: str = None, contains: str = None,
                    manual_delete: bool = False):
        """Delete messages in bulk.

        Args:
            ctx (discord.ApplicationContext): _description_
            search_past (int): Search how many messages in the past
            author (discord.Member, optional): Filter by author. Defaults to None.
            not_author (discord.Member, optional): Filter not by author. Defaults to None.
            starts_with (str, optional): Filter by starting with. Defaults to None.
            ends_with (str, optional): Filter by ending with. Defaults to None.
            contains (str, optional): Filter by containing. Defaults to None.
            manual_delete (bool, optional): Manually delete instead of bulk. Defaults to False.
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(f'{ctx.user.id} tried to use the clear command, but does not have permission to do so!')
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        embed = discord.Embed(
            title='Moderation Command Used',
            description='The command /clear was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Amount of Messages', str(search_past), True),
                discord.EmbedField('Manually delete', 'Yes' if manual_delete else 'No', True)
            ]
        )

        # get number of messages and bulk delete them
        messages = await ctx.channel.history(limit=search_past).flatten()
        # filter messages older than 2 weeks
        messages = [message for message in messages if message.created_at >
                    discord.utils.utcnow() - datetime.timedelta(weeks=2)]
        self.logger.info(f'Found {len(messages)} messages')
        # filter messages from author if author is specified
        if author is not None:
            self.logger.info(f'Filtering messages from {author}')
            messages = [
                message for message in messages if message.author == author]
            embed.add_field(name='Author filter', value=author.display_name, inline=True)
        if not_author is not None:
            self.logger.info(f'Filtering messages not from {not_author}')
            messages = [
                message for message in messages if message.author != not_author]
            embed.add_field(name='Author NOT filter', value=not_author.display_name, inline=True)

        if starts_with is not None:
            self.logger.info(f'Filtering messages starting with {starts_with}')
            messages = [
                message for message in messages if message.content.startswith(starts_with)]
            embed.add_field(name='Starts with filter', value=starts_with, inline=True)
        if ends_with is not None:
            self.logger.info(f'Filtering messages ending with {ends_with}')
            messages = [
                message for message in messages if message.content.endswith(ends_with)]
            embed.add_field(name='Ends with filter', value=ends_with, inline=True)
        if contains is not None:
            self.logger.info(f'Filtering messages containing {contains}')
            messages = [
                message for message in messages if contains in message.content]
            embed.add_field(name='Contains filter', value=contains, inline=True)
        if manual_delete:
            await ctx.defer()
            for message in messages:
                self.logger.info(f'Manually deleting message {message.id}')
                await message.delete()
            await ctx.followup.send(f'Deleted {len(messages)} messages')
        else:
            self.logger.info(f'Bulk deleting {len(messages)} messages')
            await ctx.defer()
            for chunk in [messages[i:i+100] for i in range(0, len(messages), 100)]:
                await ctx.channel.delete_messages(chunk)
            await ctx.followup.send(f'Deleted {len(messages)} messages')

        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=embed)

    @mod_group.slash_command(guild_ids=[constants.guild_id])
    async def warn(self, ctx: discord.ApplicationContext, target: discord.Member, reason: str, send_dm: bool = True):
        """Add a warning to a member.

        Args:
            ctx (discord.ApplicationContext): _description_
            target (discord.Member): The member to warn.
            reason (str): Reason for warning.
            send_dm (bool, optional): Send a DM. Defaults to True.
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(f'{ctx.user.id} tried to use the warn command, but does not have permission to do so!')
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if constants.moderator_role in [r.id for r in target.roles] and \
                constants.admin_role not in [r.id for r in ctx.user.roles] and \
                ctx.user.id != constants.bot_maintainer:
            self.logger.warning(f'{ctx.user.id} tried to warn another moderator.')
            await ctx.respond('Nice try', ephemeral=True)
            return

        await ctx.defer()

        if send_dm:
            self.logger.info(f'Sending DM to {target}')
            embed = discord.Embed(title=f'You have been warned in {ctx.guild.name}',
                                  description=f'Reason: {reason}\nBy: {ctx.user.display_name}',
                                  color=discord.Color.orange())
            try:
                await target.send(embed=embed)
            except (discord.Forbidden, discord.HTTPException):
                self.logger.info(f'Could not send DM to {target}, skipping')
                pass

        add_warning(target, reason, ctx.user)
        mod_embed = discord.Embed(
            title=f'✅ Warned {target}', description=f'Reason: {reason}\nWarned by: {ctx.user.display_name}',
            color=discord.Color.green())
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=mod_embed)
        await ctx.followup.send(embed=mod_embed)

    @mod_group.slash_command(guild_ids=[constants.guild_id])
    async def warnings(self, ctx: discord.ApplicationContext, target: discord.Member):
        """View the warnings for a member.

        Args:
            ctx (discord.ApplicationContext): _description_
            target (discord.Member): The member to view warnings for.
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(
                f'{ctx.user.id} tried to use the warnings command, but does not have permission to do so!')
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        log_embed = discord.Embed(
            title='Moderation Command Used',
            description='The command /warnings was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Target', target.display_name, True)
            ]
        )

        warnings = get_warnings(target)
        if len(warnings) == 0:
            self.logger.info(f'{target} has no warnings')
            await ctx.respond(f'{target} has no warnings')
            return

        embed = discord.Embed(title=f'Warnings for {target}', color=discord.Color.orange())
        for warning in warnings:
            self.logger.info(f'Adding warning {warnings.index(warning) + 1}')
            moderator = self.bot.get_user(warning['moderator'])
            embed.add_field(name=f'Warning {warnings.index(warning) + 1}',
                            value=f'Reason: {warning["reason"]}\nModerator: {moderator.mention}',
                            inline=warnings.index(warning) % 3 != 0)
        await ctx.respond(embed=embed)

        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)

    @mod_group.slash_command(guild_ids=[constants.guild_id])
    async def nsfw_ban(self, ctx: discord.ApplicationContext, target: discord.Member):
        """Ban someone from accessing NSFW channels.

        Args:
            ctx (discord.ApplicationContext): _description_
            target (discord.Member): The member to ban from NSFW.
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(
                f'{ctx.user.id} tried to use the NSFW ban command, but does not have permission to do so!')
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if constants.moderator_role in [r.id for r in target.roles] and \
                constants.admin_role not in [r.id for r in ctx.user.roles] and \
                ctx.user.id != constants.bot_maintainer:
            self.logger.warning(f'{ctx.user.id} tried to NSFW ban another moderator.')
            await ctx.respond('Nice try', ephemeral=True)
            return

        log_embed = discord.Embed(
            title='Moderation Command Used',
            description='The command /nsfw_ban was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Target', target.display_name, True)
            ]
        )

        await ctx.defer()
        add_nsfw_ban(target)
        self.logger.info(f'Banned {target} from NSFW')

        nsfw_role = self.bot.get_guild(constants.guild_id).get_role(1152684011748077619)
        if nsfw_role in target.roles:
            self.logger.info(f'Removing NSFW role from {target}')
            await target.remove_roles(nsfw_role, reason='NSFW ban')

        embed = discord.Embed(title=f'✅ Banned {target} from NSFW', color=discord.Color.red())
        await ctx.followup.send(embed=embed)

        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)

    @mod_group.slash_command(guild_ids=[constants.guild_id])
    async def remove_nsfw_ban(self, ctx: discord.ApplicationContext, target: discord.Member):
        """Unban someone from accessing NSFW channels.

        Args:
            ctx (discord.ApplicationContext): _description_
            target (discord.Member): The member to unban from NSFW.
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(
                f'{ctx.user.id} tried to use the NSFW unban command, but does not have permission to do so!')
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if constants.moderator_role in [r.id for r in target.roles] and \
                constants.admin_role not in [r.id for r in ctx.user.roles] and \
                ctx.user.id != constants.bot_maintainer:
            self.logger.warning(f'{ctx.user.id} tried to langauge remove NSFW ban from another moderator.')
            await ctx.respond('Nice try', ephemeral=True)
            return

        log_embed = discord.Embed(
            title='Moderation Command Used',
            description='The command /remove_nsfw_ban was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Target', target.display_name, True)
            ]
        )

        await ctx.defer()
        remove_nsfw_ban(target)
        self.logger.info(f'Removed NSFW ban for {target}')

        embed = discord.Embed(title=f'✅ Removed NSFW ban for {target}', color=discord.Color.green())
        await ctx.followup.send(embed=embed)

        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)
        
    @admin_group.slash_command(guild_ids=[constants.guild_id])
    async def add_chatpoints(self, ctx: discord.ApplicationContext, user: discord.Member, chatpoints: int):
        """Add ChatPoints to a user."""
        if constants.admin_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(
                f'{ctx.user.id} tried to use the add_chatpoints command, but does not have permission to do so!')
            await ctx.respond('You have to be admin or higher to use this command', ephemeral=True)
            return
        
        log_embed = discord.Embed(
            title='Admin Command Used',
            description='The command /add_chatpoints was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Target', user.display_name, True),
                discord.EmbedField('ChatPoints', str(chatpoints), True)
            ]
        )
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)
        
        self.logger.info(f'Adding {chatpoints} ChatPoints to {user}')
        add_chatpoints(user.id, chatpoints)
        await ctx.respond(f'Added {chatpoints} ChatPoints to {user}', ephemeral=True)
        
    @admin_group.slash_command(guild_ids=[constants.guild_id])
    async def remove_chatpoints(self, ctx: discord.ApplicationContext, user: discord.Member, chatpoints: int):
        """Remove ChatPoints from a user."""
        if constants.admin_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(
                f'{ctx.user.id} tried to use the remove_chatpoints command, but does not have permission to do so!')
            await ctx.respond('You have to be admin or higher to use this command', ephemeral=True)
            return
        
        log_embed = discord.Embed(
            title='Admin Command Used',
            description='The command /remove_chatpoints was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Target', user.display_name, True),
                discord.EmbedField('ChatPoints', str(chatpoints), True)
            ]
        )
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)
        
        self.logger.info(f'Removing {chatpoints} ChatPoints from {user}')
        remove_chatpoints(user.id, chatpoints)
        await ctx.respond(f'Removed {chatpoints} ChatPoints from {user}', ephemeral=True)
        
    @admin_group.slash_command(guild_ids=[constants.guild_id])
    async def add_cutepoints(self, ctx: discord.ApplicationContext, user: discord.Member, cutepoints: int):
        """Add CutePoints to a user."""
        if constants.admin_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(
                f'{ctx.user.id} tried to use the add_cutepoints command, but does not have permission to do so!')
            await ctx.respond('You have to be admin or higher to use this command', ephemeral=True)
            return
        
        log_embed = discord.Embed(
            title='Admin Command Used',
            description='The command /add_cutepoints was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Target', user.display_name, True),
                discord.EmbedField('CutePoints', str(cutepoints), True)
            ]
        )
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)
        
        self.logger.info(f'Adding {cutepoints} CutePoints to {user}')
        add_cutepoints(user.id, cutepoints)
        await ctx.respond(f'Added {cutepoints} CutePoints to {user}', ephemeral=True)
        
    @admin_group.slash_command(guild_ids=[constants.guild_id])
    async def remove_cutepoints(self, ctx: discord.ApplicationContext, user: discord.Member, cutepoints: int):
        """Remove CutePoints from a user."""
        if constants.admin_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(
                f'{ctx.user.id} tried to use the remove_cutepoints command, but does not have permission to do so!')
            await ctx.respond('You have to be admin or higher to use this command', ephemeral=True)
            return
        
        log_embed = discord.Embed(
            title='Admin Command Used',
            description='The command /remove_cutepoints was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Target', user.display_name, True),
                discord.EmbedField('CutePoints', str(cutepoints), True)
            ]
        )
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)
        
        self.logger.info(f'Removing {cutepoints} CutePoints from {user}')
        remove_cutepoints(user.id, cutepoints)
        await ctx.respond(f'Removed {cutepoints} CutePoints from {user}', ephemeral=True)
        
