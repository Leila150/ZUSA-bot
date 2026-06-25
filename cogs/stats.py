import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------------- SERVER INFO STATS ----------------
    @app_commands.command(
        name="stats",
        description="View server statistics"
    )
    async def stats(self, interaction: discord.Interaction):
        guild = interaction.guild

        humans = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])

        embed = discord.Embed(
            title=f"📊 {guild.name} Stats",
            color=discord.Color.blurple()
        )

        embed.add_field(name="Total Members", value=guild.member_count)
        embed.add_field(name="Humans", value=humans)
        embed.add_field(name="Bots", value=bots)
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(name="Channels", value=len(guild.channels))

        if guild.created_at:
            embed.add_field(
                name="Created",
                value=guild.created_at.strftime("%Y-%m-%d")
            )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await interaction.response.send_message(embed=embed)

    # ---------------- MEMBER JOIN TRACKING ----------------
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # DB hook (we will implement later)
        try:
            from db import db
            db.log_join(member.guild.id, member.id, str(datetime.utcnow()))
        except:
            pass

    # ---------------- MEMBER LEAVE TRACKING ----------------
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        # DB hook (we will implement later)
        try:
            from db import db
            db.log_leave(member.guild.id, member.id, str(datetime.utcnow()))
        except:
            pass


async def setup(bot):
    await bot.add_cog(Stats(bot))