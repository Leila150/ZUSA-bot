import discord
from discord.ext import commands


class MemberLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = discord.utils.get(member.guild.text_channels, name="goodbye")

        if channel:
            await channel.send(f"👋 {member.name} left the server.")


async def setup(bot):
    await bot.add_cog(MemberLeave(bot))