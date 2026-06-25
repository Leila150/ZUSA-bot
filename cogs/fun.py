import discord
import random
from discord.ext import commands
from discord import app_commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="coinflip",
        description="Flip a coin"
    )
    async def coinflip(
        self,
        interaction: discord.Interaction
    ):
        result = random.choice(
            ["Heads", "Tails"]
        )

        await interaction.response.send_message(
            f"🪙 {result}"
        )

    @app_commands.command(
        name="dice",
        description="Roll a dice"
    )
    async def dice(
        self,
        interaction: discord.Interaction
    ):
        roll = random.randint(1, 6)

        await interaction.response.send_message(
            f"🎲 You rolled a {roll}"
        )

    @app_commands.command(
        name="8ball",
        description="Ask the magic 8-ball"
    )
    async def eightball(
        self,
        interaction: discord.Interaction,
        question: str
    ):
        responses = [
            "Yes",
            "No",
            "Maybe",
            "Definitely",
            "Ask again later",
            "Very likely",
            "Unlikely",
            "Absolutely"
        ]

        await interaction.response.send_message(
            f"🎱 Question: {question}\nAnswer: {random.choice(responses)}"
        )

    @app_commands.command(
        name="choose",
        description="Choose between options"
    )
    async def choose(
        self,
        interaction: discord.Interaction,
        options: str
    ):
        choices = [
            choice.strip()
            for choice in options.split(",")
        ]

        if len(choices) < 2:
            await interaction.response.send_message(
                "❌ Provide at least two options separated by commas."
            )
            return

        await interaction.response.send_message(
            f"🤔 I choose: **{random.choice(choices)}**"
        )

    @app_commands.command(
        name="slap",
        description="Slap someone"
    )
    async def slap(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        await interaction.response.send_message(
            f"👋 {interaction.user.mention} slapped {member.mention}!"
        )


async def setup(bot):
    await bot.add_cog(Fun(bot))