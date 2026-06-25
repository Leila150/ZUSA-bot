import discord
from discord.ext import commands


class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome")

        if channel:
            await channel.send(f"👋 Welcome {member.mention} to **{member.guild.name}**!")


async def setup(bot):
    await bot.add_cog(MemberJoin(bot))