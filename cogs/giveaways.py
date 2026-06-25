import discord
import random
from discord.ext import commands
from discord import app_commands

giveaways = {}


class GiveawayView(discord.ui.View):
    def __init__(self, giveaway_id):
        super().__init__(timeout=None)
        self.giveaway_id = giveaway_id

    @discord.ui.button(
        label="Enter Giveaway",
        emoji="🎉",
        style=discord.ButtonStyle.green
    )
    async def enter(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        giveaways.setdefault(self.giveaway_id, set())
        giveaways[self.giveaway_id].add(interaction.user.id)

        await interaction.response.send_message(
            "🎉 You entered the giveaway!",
            ephemeral=True
        )


class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="giveaway",
        description="Create a giveaway"
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def giveaway(
        self,
        interaction: discord.Interaction,
        prize: str
    ):
        embed = discord.Embed(
            title="🎉 Giveaway",
            description=f"Prize: **{prize}**",
            color=discord.Color.gold()
        )

        await interaction.response.send_message(embed=embed)

        message = await interaction.original_response()

        giveaway_id = str(message.id)
        giveaways[giveaway_id] = set()

        await message.edit(
            view=GiveawayView(giveaway_id)
        )

    @app_commands.command(
        name="endgiveaway",
        description="End a giveaway"
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def endgiveaway(
        self,
        interaction: discord.Interaction,
        message_id: str
    ):
        entries = giveaways.get(message_id)

        if not entries:
            await interaction.response.send_message(
                "❌ No entries found."
            )
            return

        winner_id = random.choice(list(entries))
        winner = interaction.guild.get_member(winner_id)

        await interaction.response.send_message(
            f"🎉 Winner: {winner.mention}"
        )


async def setup(bot):
    await bot.add_cog(Giveaways(bot))