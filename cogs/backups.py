import discord
from discord.ext import commands
from discord import app_commands
import json
from datetime import datetime
from db import db


class Backups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(self, interaction: discord.Interaction):
        return interaction.user.id == self.bot.owner_id

    # ---------------- CREATE BACKUP ----------------
    @app_commands.command(
        name="backup_create",
        description="Create a full server backup"
    )
    async def backup_create(self, interaction: discord.Interaction):
        if not self.is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Not allowed.",
                ephemeral=True
            )

        guild = interaction.guild

        backup_data = {
            "guild_id": guild.id,
            "name": guild.name,
            "created_at": str(datetime.utcnow()),
            "roles": [],
            "channels": []
        }

        # ROLES
        for role in guild.roles:
            if role.is_default():
                continue

            backup_data["roles"].append({
                "name": role.name,
                "permissions": role.permissions.value,
                "color": role.color.value,
                "hoist": role.hoist,
                "mentionable": role.mentionable
            })

        # CHANNELS
        for channel in guild.channels:
            backup_data["channels"].append({
                "name": channel.name,
                "type": str(channel.type)
            })

        # SAVE TO DB (we will implement later)
        db.save_backup(
            guild.id,
            json.dumps(backup_data)
        )

        await interaction.response.send_message(
            "📦 Backup saved successfully.",
            ephemeral=True
        )

    # ---------------- LIST BACKUPS ----------------
    @app_commands.command(
        name="backup_list",
        description="List all backups"
    )
    async def backup_list(self, interaction: discord.Interaction):
        if not self.is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Not allowed.",
                ephemeral=True
            )

        backups = db.get_backups(interaction.guild.id)

        if not backups:
            return await interaction.response.send_message(
                "📭 No backups found.",
                ephemeral=True
            )

        text = "\n".join(
            f"{i+1}. Backup ID: {b[0]} | Date: {b[2]}"
            for i, b in enumerate(backups)
        )

        await interaction.response.send_message(
            f"📦 **Backups:**\n{text}",
            ephemeral=True
        )

    # ---------------- RESTORE BACKUP ----------------
    @app_commands.command(
        name="backup_restore",
        description="Restore a backup"
    )
    async def backup_restore(
        self,
        interaction: discord.Interaction,
        backup_id: int
    ):
        if not self.is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Not allowed.",
                ephemeral=True
            )

        backup = db.get_backup(backup_id)

        if not backup:
            return await interaction.response.send_message(
                "❌ Backup not found.",
                ephemeral=True
            )

        data = json.loads(backup[0])

        guild = interaction.guild

        # WARNING MESSAGE FIRST
        await interaction.response.send_message(
            "⚠️ Restoring backup... (basic version)",
            ephemeral=True
        )

        # NOTE: Real restore logic will be expanded later
        for role in data["roles"]:
            try:
                await guild.create_role(
                    name=role["name"],
                    permissions=discord.Permissions(role["permissions"]),
                    colour=discord.Colour(role["color"]),
                    hoist=role["hoist"],
                    mentionable=role["mentionable"]
                )
            except:
                pass


async def setup(bot):
    await bot.add_cog(Backups(bot))