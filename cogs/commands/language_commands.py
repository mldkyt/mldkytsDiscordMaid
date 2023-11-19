import logging
import discord
from utils.language import set_user_lang, get_user_lang, get_languages, init_lang_prefs
import constants

class LanguageCommands(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.logger = logging.getLogger('astolfo.LanguageCommands')
        self.bot = bot
        init_lang_prefs()
        super().__init__()

    
    lang_group = discord.SlashCommandGroup('language', description='Commands for changing the language of the bot.', guild_ids=[constants.guild_id])
    
    async def set_autocomplete(self, ctx: discord.AutocompleteContext):
        return get_languages()
    
    @lang_group.command(guild_ids=[constants.guild_id])
    @discord.option(name='lang', autocomplete=set_autocomplete)
    async def set(self, ctx: discord.ApplicationContext, lang: str):
        languages = get_languages()
        if lang not in languages:
            await ctx.respond('Invalid language, valid languages are: %s' % (','.join(languages)), ephemeral=True)
            return
        
        set_user_lang(ctx.author.id, lang)
        await ctx.respond('Language set to ' + lang + '.', ephemeral=True)
        
    @lang_group.command(guild_ids=[constants.guild_id])
    async def get(self, ctx: discord.ApplicationContext):
        lang = await get_user_lang(ctx.author.id)
        await ctx.respond('Your language is set to ' + lang + '.')