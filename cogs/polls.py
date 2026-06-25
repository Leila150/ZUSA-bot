import discord
from discord.ext import commands
from discord import app_commands


class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="poll",
        description="Create a poll"
    )
    async def poll(
        self,
        interaction: discord.Interaction,
        question: str
    ):
        embed = discord.Embed(
            title="📊 Poll",
            description=question,
            color=discord.Color.blurple()
        )

        embed.set_footer(
            text=f"Poll by {interaction.user}"
        )

        await interaction.response.send_message(
            embed=embed
        )

        message = await interaction.original_response()

        await message.add_reaction("👍")
        await message.add_reaction("👎")

async def setup(bot):
    await bot.add_cog(Polls(bot))