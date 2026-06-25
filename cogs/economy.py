import discord
from discord.ext import commands
from discord import app_commands
from db import db


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="balance",
        description="Check a user's balance"
    )
    async def balance(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ):
        member = member or interaction.user

        balance = db.get_balance(
            member.id,
            interaction.guild.id
        )

        await interaction.response.send_message(
            f"💰 {member.mention} has {balance} coins."
        )

    @app_commands.command(
        name="daily",
        description="Claim your daily reward"
    )
    async def daily(
        self,
        interaction: discord.Interaction
    ):
        reward = 100

        db.add_balance(
            interaction.user.id,
            interaction.guild.id,
            reward
        )

        await interaction.response.send_message(
            f"💰 You claimed {reward} coins!"
        )

    @app_commands.command(
        name="work",
        description="Work for coins"
    )
    async def work(
        self,
        interaction: discord.Interaction
    ):
        reward = 50

        db.add_balance(
            interaction.user.id,
            interaction.guild.id,
            reward
        )

        await interaction.response.send_message(
            f"🛠️ You worked and earned {reward} coins!"
        )

    @app_commands.command(
        name="give",
        description="Give coins to another user"
    )
    async def give(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        amount: int
    ):
        if amount <= 0:
            await interaction.response.send_message(
                "❌ Amount must be greater than 0."
            )
            return

        balance = db.get_balance(
            interaction.user.id,
            interaction.guild.id
        )

        if balance < amount:
            await interaction.response.send_message(
                "❌ You don't have enough coins."
            )
            return

        db.remove_balance(
            interaction.user.id,
            interaction.guild.id,
            amount
        )

        db.add_balance(
            member.id,
            interaction.guild.id,
            amount
        )

        await interaction.response.send_message(
            f"💸 Sent {amount} coins to {member.mention}"
        )

    @app_commands.command(
        name="leaderboard",
        description="Economy leaderboard"
    )
    async def leaderboard(
        self,
        interaction: discord.Interaction
    ):
        await interaction.response.send_message(
            "🏆 Economy leaderboard coming soon."
        )


async def setup(bot):
    await bot.add_cog(Economy(bot))