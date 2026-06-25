import discord
from discord.ext import commands
from discord import app_commands


class RoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role):
        super().__init__(
            label=role.name,
            style=discord.ButtonStyle.primary
        )
        self.role = role

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user

        if self.role in member.roles:
            await member.remove_roles(self.role)

            await interaction.response.send_message(
                f"➖ Removed {self.role.mention}",
                ephemeral=True
            )
        else:
            await member.add_roles(self.role)

            await interaction.response.send_message(
                f"➕ Added {self.role.mention}",
                ephemeral=True
            )


class RoleView(discord.ui.View):
    def __init__(self, role):
        super().__init__(timeout=None)
        self.add_item(RoleButton(role))


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="reactionrole",
        description="Create a role button"
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def reactionrole(
        self,
        interaction: discord.Interaction,
        role: discord.Role
    ):
        embed = discord.Embed(
            title="🎭 Reaction Roles",
            description=f"Click below to receive {role.mention}",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=RoleView(role)
        )


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))