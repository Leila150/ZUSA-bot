import discord
from discord.ext import commands
from discord import app_commands
import random
import string
from db import db


class Roblox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def generate_code(self):
        return "RBLX-" + "".join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=8
            )
        )

    # ---------------- START VERIFICATION ----------------
    @app_commands.command(
        name="verifyroblox",
        description="Link your Roblox account"
    )
    async def verifyroblox(
        self,
        interaction: discord.Interaction,
        username: str
    ):
        code = self.generate_code()

        db.save_roblox_verification(
            interaction.guild.id,
            interaction.user.id,
            username,
            code
        )

        embed = discord.Embed(
            title="🎮 Roblox Verification",
            description=(
                f"Roblox Username: **{username}**\n\n"
                f"Put this code in your Roblox profile description:\n"
                f"```{code}```\n\n"
                f"Then run `/checkroblox` to finish verification."
            ),
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    # ---------------- CHECK VERIFICATION ----------------
    @app_commands.command(
        name="checkroblox",
        description="Check your Roblox verification"
    )
    async def checkroblox(self, interaction: discord.Interaction):
        data = db.get_roblox_verification(
            interaction.guild.id,
            interaction.user.id
        )

        if not data:
            return await interaction.response.send_message(
                "❌ You haven't started verification.",
                ephemeral=True
            )

        username, code, verified = data

        if verified:
            return await interaction.response.send_message(
                "✅ You are already verified.",
                ephemeral=True
            )

        # ⚠️ REAL CHECK WILL BE ADDED LATER (ROBLOX API)
        # For now we simulate success if user says they added code

        await interaction.response.send_message(
            "🔍 Checking Roblox profile... (stub)\n"
            "If your code is in your profile, run `/forceverifyroblox`",
            ephemeral=True
        )

    # ---------------- FORCE VERIFY (TEMP) ----------------
    @app_commands.command(
        name="forceverifyroblox",
        description="Force verify (temporary)"
    )
    async def forceverifyroblox(self, interaction: discord.Interaction):
        data = db.get_roblox_verification(
            interaction.guild.id,
            interaction.user.id
        )

        if not data:
            return await interaction.response.send_message(
                "❌ No verification found.",
                ephemeral=True
            )

        username, code, verified = data

        db.set_roblox_verified(
            interaction.guild.id,
            interaction.user.id
        )

        await interaction.response.send_message(
            f"✅ Verified Roblox account: **{username}**",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Roblox(bot))