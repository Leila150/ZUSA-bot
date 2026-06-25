import discord
from discord.ext import commands


class MessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return

        print(f"Deleted message: {message.content}")


async def setup(bot):
    await bot.add_cog(MessageDelete(bot))