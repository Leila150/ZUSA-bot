import discord
from discord.ext import commands
from discord import app_commands


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Check bot latency"
    )
    async def ping(
        self,
        interaction: discord.Interaction
    ):
        latency = round(self.bot.latency * 1000)

        await interaction.response.send_message(
            f"🏓 Pong! {latency}ms"
        )

    @app_commands.command(
        name="avatar",
        description="View a user's avatar"
    )
    async def avatar(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ):
        member = member or interaction.user

        embed = discord.Embed(
            title=f"{member}'s Avatar",
            color=discord.Color.blurple()
        )

        embed.set_image(
            url=member.display_avatar.url
        )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="userinfo",
        description="View user information"
    )
    async def userinfo(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ):
        member = member or interaction.user

        embed = discord.Embed(
            title=f"User Info - {member}",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="ID",
            value=member.id,
            inline=False
        )

        embed.add_field(
            name="Joined Server",
            value=member.joined_at.strftime("%Y-%m-%d"),
            inline=False
        )

        embed.add_field(
            name="Account Created",
            value=member.created_at.strftime("%Y-%m-%d"),
            inline=False
        )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="serverinfo",
        description="View server information"
    )
    async def serverinfo(
        self,
        interaction: discord.Interaction
    ):
        guild = interaction.guild

        embed = discord.Embed(
            title=guild.name,
            color=discord.Color.green()
        )

        embed.add_field(
            name="Members",
            value=guild.member_count
        )

        embed.add_field(
            name="Roles",
            value=len(guild.roles)
        )

        embed.add_field(
            name="Channels",
            value=len(guild.channels)
        )

        if guild.icon:
            embed.set_thumbnail(
                url=guild.icon.url
            )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="say",
        description="Make the bot say something"
    )
    @app_commands.checks.has_permissions(
        manage_messages=True
    )
    async def say(
        self,
        interaction: discord.Interaction,
        message: str
    ):
        await interaction.response.send_message(
            "✅ Sent.",
            ephemeral=True
        )

        await interaction.channel.send(
            message
        )


async def setup(bot):
    await bot.add_cog(Utility(bot))