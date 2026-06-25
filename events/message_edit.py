import discord
from discord.ext import commands


class MessageEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        print(f"Edited: {before.content} -> {after.content}")


async def setup(bot):
    await bot.add_cog(MessageEdit(bot))