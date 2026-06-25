import discord


class GiveawayView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Join Giveaway", style=discord.ButtonStyle.blurple)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🎉 You joined the giveaway!", ephemeral=True)