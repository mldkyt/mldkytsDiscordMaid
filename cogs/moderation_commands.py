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


class ModerationCommands(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.logger = logging.getLogger('astolfo/ModerationCommands')
        self.bot = bot
        init()
        super().__init__()
        self.logger.info('Initialization successful')

    @discord.slash_command(guild_ids=[constants.guild_id])
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

        if search_past > 100:
            self.logger.info(f'{ctx.user.id} tried to delete more than 100 messages')
            await ctx.respond('You can only delete 100 messages at a time', ephemeral=True)
            return

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
            await ctx.channel.delete_messages(messages)
            await ctx.respond(f'Deleted {len(messages)} messages')
            
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def kick(self, ctx: discord.ApplicationContext, member: discord.Member, reason: str = None, send_dm: bool = True):
        """Kick a member from the server.

        Args:
            ctx (discord.ApplicationContext): _description_
            member (discord.Member): The member to kick
            reason (str, optional): The kick reason. Defaults to None.
            send_dm (bool, optional): Send a DM. Defaults to True.
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(f'{ctx.user.id} tried to use the kick command, but does not have permission to do so!')
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if constants.moderator_role in [r.id for r in member.roles] and ctx.user.id != constants.bot_maintainer:
            self.logger.warning(f'{ctx.user.id} tried to kick another moderator.')
            await ctx.respond('Nice try', ephemeral=True)
            return

        if reason is None:
            self.logger.info('Defaulting reason to "No reason provided"')
            reason = 'No reason provided'
        
        await ctx.defer()
        log_embed = discord.Embed(
            title='Moderation Command Used',
            description='The command /kick was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Target', member.display_name, True),
                discord.EmbedField('Reason', reason, True),
                discord.EmbedField('Send the user a DM', 'Yes' if send_dm else 'No', False)
            ]
        )

        # dm user embed with reason and give him an invitation back to the server
        if send_dm:
            self.logger.info(f'Sending DM to {member}')
            embed = discord.Embed(title=f'You have been kicked from {ctx.guild.name}',
                                  description=f'Reason: {reason}', color=discord.Color.yellow())
            embed.add_field(name='Get back',
                            value='https://discord.gg/JgFNmSwYME')
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                self.logger.info(f'Could not send DM to {member}, skipping')
                pass

        self.logger.info(f'Kicking {member}')
        await member.kick(reason=reason)
        mod_embed = discord.Embed(
            title=f'✅ Kicked {member}', description=f'Reason: {reason}\nKicked by: {ctx.user.display_name}', color=discord.Color.yellow())
        await ctx.followup.send(embed=mod_embed)
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def ban(self, ctx: discord.ApplicationContext, member: discord.Member, reason: str = None, send_dm: bool = True):
        """Ban a member from the server.

        Args:
            ctx (discord.ApplicationContext): _description_
            member (discord.Member): The member to ban
            reason (str, optional): The ban reason. Defaults to None.
            send_dm (bool, optional): Send a DM. Defaults to True.
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(f'{ctx.user.id} tried to use the ban command, but does not have permission to do so!')
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if constants.moderator_role in [r.id for r in member.roles] and ctx.user.id != constants.bot_maintainer:
            self.logger.warning(f'{ctx.user.id} tried to ban another moderator.')
            await ctx.respond('Nice try', ephemeral=True)
            return


        if reason is None:
            self.logger.info('Defaulting reason to "No reason provided"')
            reason = 'No reason provided'

        await ctx.defer()
        log_embed = discord.Embed(
            title='Moderation Command Used',
            description='The command /ban was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Target', member.display_name, True),
                discord.EmbedField('Reason', reason, True),
                discord.EmbedField('Send the user a DM', 'Yes' if send_dm else 'No', False)
            ]
        )

        # dm user embed with reason and give him an invitation back to the server
        if send_dm:
            self.logger.info(f'Sending DM to {member}')
            embed = discord.Embed(title=f'You have been banned from {ctx.guild.name}',
                                  description=f'Reason: {reason}', color=discord.Color.red())
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                self.logger.info(f'Could not send DM to {member}, skipping')
                pass

        await member.ban(reason=reason)
        mod_embed = discord.Embed(
            title=f'✅ Banned {member}', description=f'Reason: {reason}\nBanned by: {ctx.user.display_name}', color=discord.Color.red())
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=mod_embed)
        await ctx.followup.send(embed=mod_embed, ephemeral=True)
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)
        
    async def unban_autocomplete(self: discord.AutocompleteContext):        
        options = []
        
        guild = self.bot.get_guild(constants.guild_id)
        iter = 0
        async for i in guild.bans():
            if i.user.display_name.lower().startswith(self.value.lower()):
                options.append(i.user.display_name)
                iter += 1
            if iter > 9:
                break
            
        return options
        
        
        
    @discord.slash_command(guild_ids=[constants.guild_id])
    @discord.option('target', autocomplete=unban_autocomplete)
    async def unban(self, ctx: discord.ApplicationContext, target: str, reason: str = None):
        """Unban a member.

        Args:
            ctx (discord.ApplicationContext): _description_
            target (str): The target user to unban, searches in bans
            reason (str, optional): Optional reason. Defaults to None.
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(f'{ctx.user.id} tried to use the unban command, but does not have permission to do so!')
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return
        
        if reason is None:
            self.logger.info('Defaulting reason to "No reason provided"')
            reason = 'No reason provided'
        
        
        await ctx.defer()
        
        user: discord.User = None
        async for i in ctx.guild.bans():
            if i.user.display_name.lower() == target.lower():
                user = i.user
                break
        
        if user is None:
            await ctx.followup.send('User not found', ephemeral=True)
            return
        
        await ctx.guild.unban(user, reason=reason)
        mod_embed = discord.Embed(
            title=f'✅ Unbanned {target}', description=f'Reason: {reason}\nUnbanned by: {ctx.user.display_name}', color=discord.Color.green())
        await ctx.followup.send(embed=mod_embed)
        
        log_embed = discord.Embed(
            title='Moderation Command Used',
            description='The command /unban was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Target', target.display_name, True),
                discord.EmbedField('Reason', reason, True)
            ]
        )
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def timeout(self, ctx: discord.ApplicationContext, member: discord.Member, for_hours: int, for_days: int = 0, for_minutes: int = 0, for_seconds: int = 0, reason: str = None, send_dm: bool = True):
        """Time out a member.

        Args:
            ctx (discord.ApplicationContext): _description_
            member (discord.Member): The member to time out
            for_hours (int): For how many hours. Adds up with other time arguments
            for_days (int, optional): For how many days. Adds up with other time arguments. Defaults to 0.
            for_minutes (int, optional): For how many minutes. Adds up with other time arguments. Defaults to 0.
            for_seconds (int, optional): For how many seconds. Adds up with other time arguments. Defaults to 0.
            reason (str, optional): The reason for time out. Defaults to None.
            send_dm (bool, optional): Send a DM. Defaults to True.
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(f'{ctx.user.id} tried to use the timeout command, but does not have permission to do so!')
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if constants.moderator_role in [r.id for r in member.roles] and ctx.user.id != constants.bot_maintainer:
            self.logger.warning(f'{ctx.user.id} tried to mute another moderator.')
            await ctx.respond('Nice try', ephemeral=True)
            return
        
        if reason is None:
            self.logger.info('Defaulting reason to "No reason provided"')
            reason = 'No reason provided'

        await ctx.defer()
        log_embed = discord.Embed(
            title='Moderation Command Used',
            description='The command /timeout was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Target', member.display_name, True),
                discord.EmbedField('Reason', reason, True),
                discord.EmbedField('Send the user a DM', 'Yes' if send_dm else 'No', False)
            ]
        )

        if for_days == 0 and for_hours == 0 and for_minutes == 0 and for_seconds == 0:
            self.logger.info('No time specified')
            await ctx.followup.send('You have to specify a time', ephemeral=True)
            return

        total_duration = for_days * 86400 + for_hours * 3600 + for_minutes * 60 + for_seconds
        if total_duration > 604800:
            self.logger.info('Time specified is too long')
            await ctx.followup.send(f'The maximum timeout duration is 604800s', ephemeral=True)
            return

        duration = f'{for_days}d {for_hours}h {for_minutes}m {for_seconds}s'
        # dm user embed with reason
        if send_dm:
            self.logger.info(f'Sending DM to {member}')
            embed = discord.Embed(title=f'You have been timed out from {ctx.guild.name}',
                                  description=f'Reason: {reason}\nDuration: {duration}', color=discord.Color.orange())
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                self.logger.info(f'Could not send DM to {member}, skipping')
                pass

        await member.timeout_for(datetime.timedelta(seconds=total_duration), reason=reason)
        mod_embed = discord.Embed(
            title=f'✅ Timed out {member}', description=f'Reason: {reason}\nTimed out by: {ctx.user.display_name}\nDuration: {duration}', color=discord.Color.yellow())
        await ctx.followup.send(embed=mod_embed, ephemeral=True)
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)
        
    @discord.slash_command(guild_ids=[constants.guild_id])
    async def lang_timeout(self, ctx: discord.ApplicationContext, member: discord.Member, send_dm: bool = True):
        """Timeout someone for violating the language rule

        Args:
            ctx (discord.ApplicationContext): _description_
            member (discord.Member): The member to timeout
            send_dm (bool, optional): If it should send a DM. Defaults to True.
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(f'{ctx.user.id} tried to use the language timeout command, but does not have permission to do so!')
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if constants.moderator_role in [r.id for r in member.roles] and ctx.user.id != constants.bot_maintainer:
            self.logger.warning(f'{ctx.user.id} tried to langauge timeout another moderator.')
            await ctx.respond('Nice try', ephemeral=True)
            return

        await ctx.defer()
        log_embed = discord.Embed(
            title='Moderation Command Used',
            description='The command /lang_timeout was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Target', member.display_name, True),
                discord.EmbedField('Send the user a DM', 'Yes' if send_dm else 'No', False)
            ]
        )

        duration = '0d 1h 0m 0s'
        # dm user embed with reason
        if send_dm:
            self.logger.info(f'Sending DM to {member}')
            embed = discord.Embed(title=f'You have been timed out from {ctx.guild.name}',
                                  description=f'Reason: Non-English in <#1147557081721872474>, there\'s <#1157938801952428052> for other languages\nDuration: {duration}', color=discord.Color.orange())
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                self.logger.info(f'Could not send DM to {member}, skipping')
                pass

        await member.timeout_for(datetime.timedelta(seconds=3600), reason='Reason: Non-English in <#1147557081721872474>, there\'s <#1157938801952428052> for other languages')
        mod_embed = discord.Embed(
            title=f'✅ Timed out {member}', description=f'Reason: Non-English in <#1147557081721872474>, there\'s <#1157938801952428052> for other languages\nTimed out by: {ctx.user.display_name}\nDuration: {duration}', color=discord.Color.yellow())
        await ctx.followup.send(embed=mod_embed, ephemeral=True)
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def remove_timeout(self, ctx: discord.ApplicationContext, target: discord.Member, reason: str):
        """Remove time out from a member.

        Args:
            ctx (discord.ApplicationContext): _description_
            target (discord.Member): The user to remove time out from
            reason (str): Reason for time out removal
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(f'{ctx.user.id} tried to use the remove timeout command, but does not have permission to do so!')
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if constants.moderator_role in [r.id for r in target.roles] and ctx.user.id != constants.bot_maintainer:
            self.logger.warning(f'{ctx.user.id} tried to remove timeout another moderator.')
            await ctx.respond('Nice try', ephemeral=True)
            return
        
        # check if user is timed out
        if target.communication_disabled_until is None:
            self.logger.info('Target is not timed out')
            await ctx.respond(f'{target} is not timed out', ephemeral=True)
            return

        await ctx.defer()
        log_embed = discord.Embed(
            title='Moderation Command Used',
            description='The command /remove_timeout was used.',
            fields=[
                discord.EmbedField('User', ctx.user.display_name, True),
                discord.EmbedField('Target', target.display_name, True),
                discord.EmbedField('Reason', reason, True)
            ]
        )

        await target.remove_timeout(reason=reason)
        mod_embed = discord.Embed(
            title=f'✅ Removed timeout for {target}', description=f'Reason: {reason}\nBy: {ctx.user.display_name}', color=discord.Color.green())
        await ctx.followup.send(embed=mod_embed)
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
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

        if constants.moderator_role in [r.id for r in target.roles] and ctx.user.id != constants.bot_maintainer:
            self.logger.warning(f'{ctx.user.id} tried to warn another moderator.')
            await ctx.respond('Nice try', ephemeral=True)
            return

        await ctx.defer()

        if send_dm:
            self.logger.info(f'Sending DM to {target}')
            embed = discord.Embed(title=f'You have been warned in {ctx.guild.name}',
                                  description=f'Reason: {reason}\nBy: {ctx.user.display_name}', color=discord.Color.orange())
            try:
                await target.send(embed=embed)
            except discord.Forbidden:
                self.logger.info(f'Could not send DM to {target}, skipping')
                pass

        add_warning(target, reason, ctx.user)
        mod_embed = discord.Embed(
            title=f'✅ Warned {target}', description=f'Reason: {reason}\nWarned by: {ctx.user.display_name}', color=discord.Color.green())
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=mod_embed)
        await ctx.followup.send(embed=mod_embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def warnings(self, ctx: discord.ApplicationContext, target: discord.Member):
        """View the warnings for a member.

        Args:
            ctx (discord.ApplicationContext): _description_
            target (discord.Member): The member to view warnings for.
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(f'{ctx.user.id} tried to use the warnings command, but does not have permission to do so!')
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
            embed.add_field(name=f'Warning {warnings.index(warning) + 1}', value=f'Reason: {warning["reason"]}\nModerator: {moderator.mention}', inline=warnings.index(warning) % 3 != 0)
        await ctx.respond(embed=embed)
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def nsfw_ban(self, ctx: discord.ApplicationContext, target: discord.Member):
        """Ban someone from accessing NSFW channels.

        Args:
            ctx (discord.ApplicationContext): _description_
            target (discord.Member): The member to ban from NSFW.
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(f'{ctx.user.id} tried to use the NSFW ban command, but does not have permission to do so!')
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if constants.moderator_role in [r.id for r in target.roles] and ctx.user.id != constants.bot_maintainer:
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

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def remove_nsfw_ban(self, ctx: discord.ApplicationContext, target: discord.Member):
        """Unban someone from accessing NSFW channels.

        Args:
            ctx (discord.ApplicationContext): _description_
            target (discord.Member): The member to unban from NSFW.
        """
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            self.logger.warning(f'{ctx.user.id} tried to use the NSFW unban command, but does not have permission to do so!')
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if constants.moderator_role in [r.id for r in target.roles] and ctx.user.id != constants.bot_maintainer:
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