import discord


class AutoAnswer(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        super().__init__()

    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if ('msc' in msg.content or 'my summer car' in msg.content) and '165' in msg.content and ('download' in msg.content or 'dl' in msg.content or 'down' in msg.content):
            embed = discord.Embed(title='Auto Answer > My Summer Car > Development Builds', description='These builds are not available under any circumstance, even for money.')
            await msg.channel.send(embed=embed)

        if ('msc' in msg.content or 'my summer car' in msg.content) and 'modding' in msg.content:
            embed = discord.Embed(title='Auto Answer > My Summer Car > How To Get Started In Making Mods', description='You can get stated with modding using tutorials that I made on my YouTube channel.')
            await msg.channel.send(embed=embed)

        if 'next' in msg.content and 'video' in msg.content:
            embed = discord.Embed(title='Auto Answer > YouTube > Next Video', description='The next video will be released when it is done.')
            await msg.channel.send(embed=embed)
