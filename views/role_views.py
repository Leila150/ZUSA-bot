import discord


class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Choose a role",
        options=[
            discord.SelectOption(label="Member", value="member"),
            discord.SelectOption(label="Gamer", value="gamer")
        ]
    )
    async def select_role(self, interaction: discord.Interaction, select: discord.ui.Select):
        role = discord.utils.get(interaction.guild.roles, name=select.values[0])

        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Role added!", ephemeral=True)