import datetime

import discord

import constants


class ModerationCommands(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        super().__init__()

    @discord.slash_command()
    async def clear(self, ctx: discord.ApplicationContext, search_past: int,
                    author: discord.Member = None, not_author: discord.Member = None,
                    starts_with: str = None, ends_with: str = None, contains: str = None,
                    manual_delete: bool = False, send_public: bool = False):
        if not ctx.user.guild_permissions.manage_messages:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        if search_past > 100:
            await ctx.respond('You can only delete 100 messages at a time', ephemeral=True)
            return

        # get number of messages and bulk delete them
        messages = await ctx.channel.history(limit=search_past).flatten()
        # filter messages older than 2 weeks
        messages = [message for message in messages if message.created_at > discord.utils.utcnow() - datetime.timedelta(weeks=2)]
        # filter messages from author if author is specified
        if author is not None:
            messages = [message for message in messages if message.author == author]
        if not_author is not None:
            messages = [message for message in messages if message.author != not_author]

        if starts_with is not None:
            messages = [message for message in messages if message.content.startswith(starts_with)]
        if ends_with is not None:
            messages = [message for message in messages if message.content.endswith(ends_with)]
        if contains is not None:
            messages = [message for message in messages if contains in message.content]
        if manual_delete:
            await ctx.defer(ephemeral=not send_public)
            for message in messages:
                await message.delete()
            await ctx.followup.send(f'Deleted {len(messages)} messages', ephemeral=not send_public)
        else:
            await ctx.channel.delete_messages(messages)
            await ctx.respond(f'Deleted {len(messages)} messages', ephemeral=not send_public)

    @discord.slash_command()
    async def kick(self, ctx: discord.ApplicationContext, member: discord.Member, reason: str = None, send_public: bool = False, send_dm=True):
        if not ctx.user.guild_permissions.kick_members:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        await ctx.defer(ephemeral=not send_public)

        # dm user embed with reason and give him an invitation back to the server
        if send_dm:
            embed = discord.Embed(title='You have been kicked from mldkyt\'s bedroom', description=f'Reason: {reason}', color=discord.Color.yellow())
            embed.add_field(name='Get back', value='https://discord.gg/JgFNmSwYME')
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                pass

        await member.kick(reason=reason)
        mod_embed = discord.Embed(title=f'✅ Kicked {member}', description=f'Reason: {reason}\nKicked by: {ctx.user.display_name}', color=discord.Color.yellow())
        await ctx.followup.send(embed=mod_embed, ephemeral=True)

    @discord.slash_command()
    async def ban(self, ctx: discord.ApplicationContext, member: discord.Member, reason: str = None, send_public: bool = False, send_dm=True):
        if not ctx.user.guild_permissions.ban_members:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        await ctx.defer(ephemeral=not send_public)

        # dm user embed with reason and give him an invitation back to the server
        if send_dm:
            embed = discord.Embed(title='You have been banned from mldkyt\' bedroom', description=f'Reason: {reason}', color=discord.Color.red())
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                pass

        await member.ban(reason=reason)
        mod_embed = discord.Embed(title=f'✅ Banned {member}', description=f'Reason: {reason}\nBanned by: {ctx.user.display_name}', color=discord.Color.red())
        await ctx.followup.send(embed=mod_embed, ephemeral=True)

    @discord.slash_command()
    async def timeout(self, ctx: discord.ApplicationContext, member: discord.Member, for_hours: int, for_days: int = 0, for_minutes: int = 0, for_seconds: int = 0, reason: str = None, send_public: bool = False, send_dm=True):
        if not ctx.user.guild_permissions.kick_members:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return

        await ctx.defer(ephemeral=not send_public)

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
            embed = discord.Embed(title='You have been timed out from mldkyt\' bedroom', description=f'Reason: {reason}\nDuration: {duration}', color=discord.Color.orange())
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                pass


        await member.timeout_for(datetime.timedelta(seconds=total_duration), reason=reason)
        mod_embed = discord.Embed(title=f'✅ Timed out {member}', description=f'Reason: {reason}\nTimed out by: {ctx.user.display_name}\nDuration: {duration}', color=discord.Color.yellow())
        await ctx.followup.send(embed=mod_embed, ephemeral=True)
