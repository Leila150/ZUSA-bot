import discord
from discord.ext import commands
from discord import app_commands


class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close Ticket",
        style=discord.ButtonStyle.red,
        emoji="🔒"
    )
    async def close_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "🔒 Closing ticket...",
            ephemeral=True
        )

        await interaction.channel.delete()


class TicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Create Ticket",
        style=discord.ButtonStyle.green,
        emoji="🎫"
    )
    async def create_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        guild = interaction.guild

        existing = discord.utils.get(
            guild.channels,
            name=f"ticket-{interaction.user.name.lower()}"
        )

        if existing:
            await interaction.response.send_message(
                f"You already have a ticket: {existing.mention}",
                ephemeral=True
            )
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),
            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True
            )
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            overwrites=overwrites
        )

        await channel.send(
            f"{interaction.user.mention}",
            view=CloseTicket()
        )

        await interaction.response.send_message(
            f"✅ Ticket created: {channel.mention}",
            ephemeral=True
        )


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ticketpanel",
        description="Create a ticket panel"
    )
    @app_commands.checks.has_permissions(
        manage_channels=True
    )
    async def ticketpanel(
        self,
        interaction: discord.Interaction
    ):
        embed = discord.Embed(
            title="🎫 Support Tickets",
            description="Press the button below to open a ticket.",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=TicketPanel()
        )


async def setup(bot):
    await bot.add_cog(Tickets(bot))