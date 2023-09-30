import datetime
import json

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
        self.bot = bot
        init()
        super().__init__()

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def clear(self, ctx: discord.ApplicationContext, search_past: int,
                    author: discord.Member = None, not_author: discord.Member = None,
                    starts_with: str = None, ends_with: str = None, contains: str = None,
                    manual_delete: bool = False):
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
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
            await ctx.respond('You can only delete 100 messages at a time', ephemeral=True)
            return

        # get number of messages and bulk delete them
        messages = await ctx.channel.history(limit=search_past).flatten()
        # filter messages older than 2 weeks
        messages = [message for message in messages if message.created_at >
                    discord.utils.utcnow() - datetime.timedelta(weeks=2)]
        # filter messages from author if author is specified
        if author is not None:
            messages = [
                message for message in messages if message.author == author]
            embed.add_field(name='Author filter', value=author.display_name, inline=True)
        if not_author is not None:
            messages = [
                message for message in messages if message.author != not_author]
            embed.add_field(name='Author NOT filter', value=not_author.display_name, inline=True)

        if starts_with is not None:
            messages = [
                message for message in messages if message.content.startswith(starts_with)]
            embed.add_field(name='Starts with filter', value=starts_with, inline=True)
        if ends_with is not None:
            messages = [
                message for message in messages if message.content.endswith(ends_with)]
            embed.add_field(name='Ends with filter', value=ends_with, inline=True)
        if contains is not None:
            messages = [
                message for message in messages if contains in message.content]
            embed.add_field(name='Contains filter', value=contains, inline=True)
        if manual_delete:
            await ctx.defer()
            for message in messages:
                await message.delete()
            await ctx.followup.send(f'Deleted {len(messages)} messages')
        else:
            await ctx.channel.delete_messages(messages)
            await ctx.respond(f'Deleted {len(messages)} messages')
            
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def kick(self, ctx: discord.ApplicationContext, member: discord.Member, reason: str = None, send_dm: bool = True):
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

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
            embed = discord.Embed(title=f'You have been kicked from {ctx.guild.name}',
                                  description=f'Reason: {reason}', color=discord.Color.yellow())
            embed.add_field(name='Get back',
                            value='https://discord.gg/JgFNmSwYME')
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                pass

        await member.kick(reason=reason)
        mod_embed = discord.Embed(
            title=f'✅ Kicked {member}', description=f'Reason: {reason}\nKicked by: {ctx.user.display_name}', color=discord.Color.yellow())
        await ctx.followup.send(embed=mod_embed)
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def ban(self, ctx: discord.ApplicationContext, member: discord.Member, reason: str = None, send_dm: bool = True):
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

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
            embed = discord.Embed(title=f'You have been banned from {ctx.guild.name}',
                                  description=f'Reason: {reason}', color=discord.Color.red())
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                pass

        await member.ban(reason=reason)
        mod_embed = discord.Embed(
            title=f'✅ Banned {member}', description=f'Reason: {reason}\nBanned by: {ctx.user.display_name}', color=discord.Color.red())
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=mod_embed)
        await ctx.followup.send(embed=mod_embed, ephemeral=True)
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def timeout(self, ctx: discord.ApplicationContext, member: discord.Member, for_hours: int, for_days: int = 0, for_minutes: int = 0, for_seconds: int = 0, reason: str = None, send_dm: bool = True):
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

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
            await ctx.followup.send('You have to specify a time', ephemeral=True)
            return

        total_duration = for_days * 86400 + for_hours * 3600 + for_minutes * 60 + for_seconds
        if total_duration > 604800:
            await ctx.followup.send(f'The maximum timeout duration is 604800s', ephemeral=True)
            return

        duration = f'{for_days}d {for_hours}h {for_minutes}m {for_seconds}s'
        # dm user embed with reason
        if send_dm:
            embed = discord.Embed(title=f'You have been timed out from {ctx.guild.name}',
                                  description=f'Reason: {reason}\nDuration: {duration}', color=discord.Color.orange())
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                pass

        await member.timeout_for(datetime.timedelta(seconds=total_duration), reason=reason)
        mod_embed = discord.Embed(
            title=f'✅ Timed out {member}', description=f'Reason: {reason}\nTimed out by: {ctx.user.display_name}\nDuration: {duration}', color=discord.Color.yellow())
        await ctx.followup.send(embed=mod_embed, ephemeral=True)
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def remove_timeout(self, ctx: discord.ApplicationContext, target: discord.Member, reason: str):
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
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
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        await ctx.defer()

        if send_dm:
            embed = discord.Embed(title=f'You have been warned in {ctx.guild.name}',
                                  description=f'Reason: {reason}\nBy: {ctx.user.display_name}', color=discord.Color.orange())
            try:
                await target.send(embed=embed)
            except discord.Forbidden:
                pass

        add_warning(target, reason, ctx.user)
        mod_embed = discord.Embed(
            title=f'✅ Warned {target}', description=f'Reason: {reason}\nWarned by: {ctx.user.display_name}', color=discord.Color.green())
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=mod_embed)
        await ctx.followup.send(embed=mod_embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def warnings(self, ctx: discord.ApplicationContext, target: discord.Member):
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
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
            await ctx.respond(f'{target} has no warnings')
            return

        embed = discord.Embed(title=f'Warnings for {target}', color=discord.Color.orange())
        for warning in warnings:
            moderator = self.bot.get_user(warning['moderator'])
            embed.add_field(name=f'Warning {warnings.index(warning) + 1}', value=f'Reason: {warning["reason"]}\nModerator: {moderator.mention}', inline=warnings.index(warning) % 3 != 0)
        await ctx.respond(embed=embed)
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def nsfw_ban(self, ctx: discord.ApplicationContext, target: discord.Member):
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
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

        nsfw_role = self.bot.get_guild(constants.guild_id).get_role(1152684011748077619)
        if nsfw_role in target.roles:
            await target.remove_roles(nsfw_role, reason='NSFW ban')

        embed = discord.Embed(title=f'✅ Banned {target} from NSFW', color=discord.Color.red())
        await ctx.followup.send(embed=embed)
        
        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)

    @discord.slash_command(guild_ids=[constants.guild_id])
    async def remove_nsfw_ban(self, ctx: discord.ApplicationContext, target: discord.Member):
        if constants.moderator_role not in [r.id for r in ctx.user.roles]:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
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

        embed = discord.Embed(title=f'✅ Removed NSFW ban for {target}', color=discord.Color.green())
        await ctx.followup.send(embed=embed)

        log_channel = self.bot.get_channel(constants.log_channel)
        await log_channel.send(embed=log_embed)