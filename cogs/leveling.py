import discord
from discord.ext import commands
from discord import app_commands
from db import db


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        db.add_xp(
            message.author.id,
            message.guild.id,
            5
        )

    @app_commands.command(
        name="rank",
        description="View your rank"
    )
    async def rank(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ):
        member = member or interaction.user

        level = db.get_level(
            member.id,
            interaction.guild.id
        )

        xp = db.get_xp(
            member.id,
            interaction.guild.id
        )

        embed = discord.Embed(
            title=f"{member}'s Rank",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Level",
            value=str(level)
        )

        embed.add_field(
            name="XP",
            value=str(xp)
        )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="leaderboard",
        description="XP leaderboard"
    )
    async def leaderboard(
        self,
        interaction: discord.Interaction
    ):
        await interaction.response.send_message(
            "🏆 Level leaderboard coming soon."
        )

    @app_commands.command(
        name="addxp",
        description="Add XP to a user"
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def addxp(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        amount: int
    ):
        db.add_xp(
            member.id,
            interaction.guild.id,
            amount
        )

        await interaction.response.send_message(
            f"✅ Added {amount} XP to {member.mention}"
        )


async def setup(bot):
    await bot.add_cog(Leveling(bot))