import discord
from discord.ext import commands
from discord import app_commands
from db import db

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Set Logs",
        style=discord.ButtonStyle.red,
        emoji="📝"
    )
    async def set_logs(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        db.set_log_channel(
            interaction.guild.id,
            interaction.channel.id
        )

        await interaction.response.send_message(
            "✅ This channel has been set as the logs channel.",
            ephemeral=True
        )

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="setup",
        description="Open the bot setup panel"
    )
    async def setup(
        self,
        interaction: discord.Interaction
    ):
        embed = discord.Embed(
            title="⚙️ Bot Setup",
            description=(
                "Use the buttons below to configure the bot.\n\n"
                "📝 **Set Logs**\n"
                "Sets the current channel as the logs channel."
            ),
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=SetupView(),
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Setup(bot))    async def setup(
        self,
        interaction: discord.Interaction
    ):
        embed = discord.Embed(
            title="⚙️ Bot Setup",
            description="Use the buttons below to configure the bot.",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=SetupView(),
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Setup(bot))
