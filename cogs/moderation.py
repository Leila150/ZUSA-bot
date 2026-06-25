import discord
from discord.ext import commands
from discord import app_commands
from db import db

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="warn", description="Warn a member")
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided"
    ):
        db.add_warning(member.id, interaction.guild.id, reason)

        await interaction.response.send_message(
            f"⚠️ {member.mention} was warned.\nReason: {reason}"
        )

    @app_commands.command(name="warnings", description="View a member's warnings")
    async def warnings(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        warns = db.get_warnings(member.id, interaction.guild.id)

        if not warns:
            return await interaction.response.send_message(
                "No warnings found."
            )

        text = "\n".join(f"{i+1}. {w[0]}" for i, w in enumerate(warns))

        embed = discord.Embed(
            title=f"Warnings for {member}",
            description=text,
            color=discord.Color.orange()
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kick", description="Kick a member")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided"
    ):
        await member.kick(reason=reason)

        await interaction.response.send_message(
            f"👢 Kicked {member.mention}"
        )

    @app_commands.command(name="ban", description="Ban a member")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided"
    ):
        await member.ban(reason=reason)

        await interaction.response.send_message(
            f"🔨 Banned {member.mention}"
        )

async def setup(bot):
    await bot.add_cog(Moderation(bot))
