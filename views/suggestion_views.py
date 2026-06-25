import discord


class SuggestionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Upvote", style=discord.ButtonStyle.green)
    async def upvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("👍 Upvoted!", ephemeral=True)

    @discord.ui.button(label="Downvote", style=discord.ButtonStyle.red)
    async def downvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("👎 Downvoted!", ephemeral=True)