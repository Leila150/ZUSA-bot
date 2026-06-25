import discord
import asyncio
from discord.ext import commands
from discord import app_commands


class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="remind",
        description="Set a reminder"
    )
    async def remind(
        self,
        interaction: discord.Interaction,
        minutes: int,
        reminder: str
    ):
        await interaction.response.send_message(
            f"⏰ Reminder set for {minutes} minute(s).",
            ephemeral=True
        )

        await asyncio.sleep(minutes * 60)

        try:
            await interaction.user.send(
                f"⏰ Reminder:\n{reminder}"
            )
        except discord.Forbidden:
            pass

    @app_commands.command(
        name="timer",
        description="Start a timer"
    )
    async def timer(
        self,
        interaction: discord.Interaction,
        seconds: int
    ):
        await interaction.response.send_message(
            f"⏳ Timer started for {seconds} seconds."
        )

        await asyncio.sleep(seconds)

        await interaction.followup.send(
            f"⏰ {interaction.user.mention}, your timer has ended!"
        )


async def setup(bot):
    await bot.add_cog(Reminders(bot))