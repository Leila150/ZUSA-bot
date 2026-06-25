import discord
from discord.ext import commands
from discord import app_commands
import os


class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(self, interaction: discord.Interaction):
        return interaction.user.id == self.bot.owner_id

    @app_commands.command(
        name="sync",
        description="Sync slash commands (owner only)"
    )
    async def sync(self, interaction: discord.Interaction):
        if not self.is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Not allowed.",
                ephemeral=True
            )

        synced = await self.bot.tree.sync()

        await interaction.response.send_message(
            f"✅ Synced {len(synced)} commands.",
            ephemeral=True
        )

    @app_commands.command(
        name="reload",
        description="Reload a cog (owner only)"
    )
    async def reload(
        self,
        interaction: discord.Interaction,
        cog: str
    ):
        if not self.is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Not allowed.",
                ephemeral=True
            )

        try:
            await self.bot.reload_extension(f"cogs.{cog}")

            await interaction.response.send_message(
                f"🔁 Reloaded cogs.{cog}",
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error:\n```{e}```",
                ephemeral=True
            )

    @app_commands.command(
        name="load",
        description="Load a cog (owner only)"
    )
    async def load(
        self,
        interaction: discord.Interaction,
        cog: str
    ):
        if not self.is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Not allowed.",
                ephemeral=True
            )

        try:
            await self.bot.load_extension(f"cogs.{cog}")

            await interaction.response.send_message(
                f"📦 Loaded cogs.{cog}",
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error:\n```{e}```",
                ephemeral=True
            )

    @app_commands.command(
        name="unload",
        description="Unload a cog (owner only)"
    )
    async def unload(
        self,
        interaction: discord.Interaction,
        cog: str
    ):
        if not self.is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Not allowed.",
                ephemeral=True
            )

        try:
            await self.bot.unload_extension(f"cogs.{cog}")

            await interaction.response.send_message(
                f"🗑 Unloaded cogs.{cog}",
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error:\n```{e}```",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Developer(bot))