import discord
from discord.ext import commands
from discord import app_commands


class SuggestionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Upvote",
        emoji="👍",
        style=discord.ButtonStyle.green
    )
    async def upvote(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "👍 Vote recorded.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Downvote",
        emoji="👎",
        style=discord.ButtonStyle.red
    )
    async def downvote(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "👎 Vote recorded.",
            ephemeral=True
        )


class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="suggest",
        description="Create a suggestion"
    )
    async def suggest(
        self,
        interaction: discord.Interaction,
        suggestion: str
    ):
        embed = discord.Embed(
            title="💡 New Suggestion",
            description=suggestion,
            color=discord.Color.gold()
        )

        embed.set_footer(
            text=f"Suggested by {interaction.user}"
        )

        await interaction.response.send_message(
            embed=embed,
            view=SuggestionView()
        )


async def setup(bot):
    await bot.add_cog(Suggestions(bot))