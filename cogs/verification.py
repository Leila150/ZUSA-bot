import discord
from discord.ext import commands
from discord import app_commands


class VerifyView(discord.ui.View):
    def __init__(self, role: discord.Role):
        super().__init__(timeout=None)
        self.role = role

    @discord.ui.button(
        label="Verify",
        emoji="✅",
        style=discord.ButtonStyle.green
    )
    async def verify(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        member = interaction.user

        if self.role in member.roles:
            await interaction.response.send_message(
                "✅ You are already verified.",
                ephemeral=True
            )
            return

        try:
            await member.add_roles(self.role)

            await interaction.response.send_message(
                f"✅ You have been verified and received {self.role.mention}.",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I don't have permission to give that role.",
                ephemeral=True
            )


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="verificationpanel",
        description="Create a verification panel"
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def verificationpanel(
        self,
        interaction: discord.Interaction,
        role: discord.Role
    ):
        embed = discord.Embed(
            title="✅ Verification",
            description=(
                "Press the button below to verify yourself "
                "and receive access to the server."
            ),
            color=discord.Color.green()
        )

        await interaction.response.send_message(
            embed=embed,
            view=VerifyView(role)
        )


async def setup(bot):
    await bot.add_cog(Verification(bot))