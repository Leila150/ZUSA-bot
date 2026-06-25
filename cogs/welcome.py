import discord
from discord.ext import commands
from db import db


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild):
        channel_id = db.get_log_channel(guild.id)

        if not channel_id:
            return None

        return guild.get_channel(channel_id)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await self.get_log_channel(member.guild)

        if not channel:
            return

        embed = discord.Embed(
            title="🎉 Welcome!",
            description=f"Welcome to the server, {member.mention}!",
            color=discord.Color.green()
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = await self.get_log_channel(member.guild)

        if not channel:
            return

        embed = discord.Embed(
            title="👋 Goodbye!",
            description=f"{member} has left the server.",
            color=discord.Color.red()
        )

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Welcome(bot))