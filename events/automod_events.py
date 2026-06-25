import discord
from discord.ext import commands

class AutoModEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bad_words = ["badword1", "badword2"]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if not message.guild:
            return

        content = message.content.lower()

        for word in self.bad_words:
            if word in content:
                await message.delete()
                return

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(AutoModEvents(bot))