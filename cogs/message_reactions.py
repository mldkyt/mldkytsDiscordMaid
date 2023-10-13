import discord
import logging
import re
import constants

class MessageReactions(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.MessageReactions')
        self.bot = bot
        super().__init__()
        self.logger.info('MessageReactions initialization successful')
        
    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        
        match = re.search(r':3+', msg.clean_content)
        if match is not None:
            emote = self.bot.get_emoji(1161378541561204827) # :3 emoji
            await msg.add_reaction(emote)
            
        match = re.search(r'(owo|uwu)', msg.clean_content)
        if match is not None:
            emote = self.bot.get_emoji(1161378540059627621) # owo emoji
            await msg.add_reaction(emote)
            
        match = re.search(r'ny+a+', msg.clean_content)
        if match is not None:
            emote = self.bot.get_emoji(1161378537719205989) # nya emoji
            await msg.add_reaction(emote)
            
        match = re.search(r'meo+w+', msg.clean_content)
        if match is not None:
            emote = self.bot.get_emoji(1161378537719205989) # nya emoji
            await msg.add_reaction(emote)
            
        match = re.search(r'mr+', msg.clean_content)
        if match is not None:
            emote = self.bot.get_emoji(1161378537719205989) # nya emoji
            await msg.add_reaction(emote)
            
    @discord.slash_command(guild_ids=[constants.guild_id])
    async def react_to_past_message(self, ctx: discord.ApplicationContext):
        if ctx.user.id != constants.bot_maintainer:
            await ctx.respond('You are not allowed to use this command.', ephemeral=True)
            return
        
        await ctx.defer()
        
        async for msg in ctx.channel.history(limit=100):
            match = re.search(r':3+', msg.clean_content)
            if match is not None:
                emote = self.bot.get_emoji(1161378541561204827)
                await msg.add_reaction(emote)
                
            match = re.search(r'(owo|uwu)', msg.clean_content)
            if match is not None:
                emote = self.bot.get_emoji(1161378540059627621)
                await msg.add_reaction(emote)
                
            match = re.search(r'ny+a+', msg.clean_content)
            if match is not None:
                emote = self.bot.get_emoji(1161378537719205989)
                await msg.add_reaction(emote)
                
            match = re.search(r'meo+w+', msg.clean_content)
            if match is not None:
                emote = self.bot.get_emoji(1161378537719205989)
                await msg.add_reaction(emote)
                
            match = re.search(r'mr+', msg.clean_content)
            if match is not None:
                emote = self.bot.get_emoji(1161378537719205989)
                await msg.add_reaction(emote)
                
        await ctx.followup.send('Done!', ephemeral=True)
