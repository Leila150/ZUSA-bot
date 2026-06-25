import discord


class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green)
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="Verified")

        if role:
            await interaction.user.add_roles(role)

        await interaction.response.send_message("✅ Verified!", ephemeral=True)