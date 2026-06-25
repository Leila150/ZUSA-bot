import discord
from discord.ext import commands
from db import db


class Logging(commands.Cog):
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
            title="Member Joined",
            description=f"{member.mention} joined the server.",
            color=discord.Color.green()
        )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = await self.get_log_channel(member.guild)

        if not channel:
            return

        embed = discord.Embed(
            title="Member Left",
            description=f"{member} left the server.",
            color=discord.Color.red()
        )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.guild:
            return

        channel = await self.get_log_channel(message.guild)

        if not channel:
            return

        embed = discord.Embed(
            title="Message Deleted",
            color=discord.Color.orange()
        )

        embed.add_field(
            name="Author",
            value=message.author.mention,
            inline=False
        )

        embed.add_field(
            name="Channel",
            value=message.channel.mention,
            inline=False
        )

        embed.add_field(
            name="Content",
            value=message.content[:1000] if message.content else "No content",
            inline=False
        )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or not before.guild:
            return

        if before.content == after.content:
            return

        channel = await self.get_log_channel(before.guild)

        if not channel:
            return

        embed = discord.Embed(
            title="Message Edited",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Author",
            value=before.author.mention,
            inline=False
        )

        embed.add_field(
            name="Before",
            value=before.content[:1000] if before.content else "No content",
            inline=False
        )

        embed.add_field(
            name="After",
            value=after.content[:1000] if after.content else "No content",
            inline=False
        )

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logging(bot))