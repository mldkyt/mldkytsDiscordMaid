import discord


class ChatLimit(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        super().__init__()

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        # warn user that their message is about to hit the limit above 800
        if len(message.content) > 800:
            msg = await message.reply(f'{message.author.mention} your message is about to hit length {len(message.content)}/1000')
            await msg.delete(delay=5)

        # delete if above 1000
        if len(message.content) > 1000:
            await message.delete()
            msg = await message.channel.send(f'{message.author.mention} your message is too long! (max 1000 characters)')
            await msg.delete(delay=5)
