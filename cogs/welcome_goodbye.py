import discord

import constants


class WelcomeGoodbye(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        super().__init__()

    @discord.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(constants.welcome_channel)
        await channel.send(f':green_circle: Welcome {member.display_name} to mldkyt\'s Discord!')

    @discord.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = self.bot.get_channel(constants.welcome_channel)
        await channel.send(f':red_circle: Goodbye {member.display_name}!')
