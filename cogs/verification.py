
import logging
import discord
import constants

class Verification(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.Verification')
        self.bot = bot
        super().__init__()
        self.logger.info('Loaded cog Verification')
    
    @discord.slash_command(guild_ids=[constants.guild_id])
    async def verify_all_existing_members(self, ctx: discord.ApplicationContext):
        if ctx.user.id != constants.bot_maintainer:
            await ctx.respond('You are not allowed to use this command', ephemeral=True)
            return
        
        members = ctx.guild.members
        members = [member for member in members if not member.bot]
        await ctx.respond('Processing status will be sent in this channel', ephemeral=True)
        message = await ctx.channel.send('Verifying all existing members...\n0/' + str(len(members)))
        
        for i, member in enumerate(members):
            await member.add_roles(ctx.guild.get_role(constants.verified_role))
            await message.edit(content='Verifying all existing members...\n' + str(i + 1) + '/' + str(len(members)))
            
        await message.edit(content='Verifying all existing members...\nDone!')
