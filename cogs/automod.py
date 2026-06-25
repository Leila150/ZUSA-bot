from discord.ext import commands
from discord import app_commands
import discord

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bad_words = [
            "badword1",
            "badword2",
            "badword3"
        ]

    @app_commands.command(
        name="automod",
        description="Enable or disable automod"
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def automod(
        self,
        interaction: discord.Interaction,
        enabled: bool
    ):
        if enabled:
            self.bot.automod_enabled = True
            await interaction.response.send_message(
                "✅ Automod enabled."
            )
        else:
            self.bot.automod_enabled = False
            await interaction.response.send_message(
                "❌ Automod disabled."
            )

    @commands.Cog.listener()
    async def on_message(
        self,
        message
    ):
        if message.author.bot:
            return

        if not getattr(
            self.bot,
            "automod_enabled",
            True
        ):
            return

        content = message.content.lower()

        for word in self.bad_words:
            if word in content:
                await message.delete()

                await message.channel.send(
                    f"⚠️ {message.author.mention}, that word is not allowed.",
                    delete_after=5
                )

                return

        invite_patterns = [
            "discord.gg/",
            "discord.com/invite/"
        ]

        for pattern in invite_patterns:
            if pattern in content:
                await message.delete()

                await message.channel.send(
                    f"🚫 {message.author.mention}, invite links are not allowed.",
                    delete_after=5
                )

                return

        await self.bot.process_commands(
            message
        )

async def setup(bot):
    await bot.add_cog(
        Automod(bot)
    )