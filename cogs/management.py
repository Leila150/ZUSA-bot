from discord.ext import commands
from discord import app_commands
import discord

class Management(commands.Cog):
def init(self, bot):
self.bot = bot

@app_commands.command(
    name="lock",
    description="Lock the current channel"
)
@app_commands.checks.has_permissions(
    manage_channels=True
)
async def lock(
    self,
    interaction: discord.Interaction
):
    await interaction.channel.set_permissions(
        interaction.guild.default_role,
        send_messages=False
    )

    await interaction.response.send_message(
        "🔒 Channel locked."
    )

@app_commands.command(
    name="unlock",
    description="Unlock the current channel"
)
@app_commands.checks.has_permissions(
    manage_channels=True
)
async def unlock(
    self,
    interaction: discord.Interaction
):
    await interaction.channel.set_permissions(
        interaction.guild.default_role,
        send_messages=True
    )

    await interaction.response.send_message(
        "🔓 Channel unlocked."
    )

@app_commands.command(
    name="slowmode",
    description="Set channel slowmode"
)
@app_commands.checks.has_permissions(
    manage_channels=True
)
async def slowmode(
    self,
    interaction: discord.Interaction,
    seconds: int
):
    await interaction.channel.edit(
        slowmode_delay=seconds
    )

    await interaction.response.send_message(
        f"🐢 Slowmode set to {seconds} seconds."
    )

@app_commands.command(
    name="createchannel",
    description="Create a text channel"
)
@app_commands.checks.has_permissions(
    manage_channels=True
)
async def createchannel(
    self,
    interaction: discord.Interaction,
    name: str
):
    await interaction.guild.create_text_channel(
        name
    )

    await interaction.response.send_message(
        f"✅ Created channel: {name}"
    )

@app_commands.command(
    name="deletechannel",
    description="Delete a text channel"
)
@app_commands.checks.has_permissions(
    manage_channels=True
)
async def deletechannel(
    self,
    interaction: discord.Interaction,
    channel: discord.TextChannel
):
    await interaction.response.send_message(
        f"🗑 Deleting {channel.mention}"
    )

    await channel.delete()

@app_commands.command(
    name="createrole",
    description="Create a role"
)
@app_commands.checks.has_permissions(
    manage_roles=True
)
async def createrole(
    self,
    interaction: discord.Interaction,
    name: str
):
    await interaction.guild.create_role(
        name=name
    )

    await interaction.response.send_message(
        f"✅ Created role: {name}"
    )

@app_commands.command(
    name="deleterole",
    description="Delete a role"
)
@app_commands.checks.has_permissions(
    manage_roles=True
)
async def deleterole(
    self,
    interaction: discord.Interaction,
    role: discord.Role
):
    await role.delete()

    await interaction.response.send_message(
        f"🗑 Deleted role: {role.name}"
    )

@app_commands.command(
    name="giverole",
    description="Give a role"
)
@app_commands.checks.has_permissions(
    manage_roles=True
)
async def giverole(
    self,
    interaction: discord.Interaction,
    member: discord.Member,
    role: discord.Role
):
    await member.add_roles(role)

    await interaction.response.send_message(
        f"✅ Gave {role.mention} to {member.mention}"
    )

@app_commands.command(
    name="removerole",
    description="Remove a role"
)
@app_commands.checks.has_permissions(
    manage_roles=True
)
async def removerole(
    self,
    interaction: discord.Interaction,
    member: discord.Member,
    role: discord.Role
):
    await member.remove_roles(role)

    await interaction.response.send_message(
        f"✅ Removed {role.mention} from {member.mention}"
    )

@app_commands.command(
    name="refreshchannel",
    description="Clone and refresh the current channel"
)
@app_commands.checks.has_permissions(
    administrator=True
)
async def refreshchannel(
    self,
    interaction: discord.Interaction
):
    new_channel = await interaction.channel.clone(
        reason=f"Refreshed by {interaction.user}"
    )

    await interaction.response.send_message(
        "🔄 Refreshing channel..."
    )

    await interaction.channel.delete()

    await new_channel.send(
        "✅ Channel refreshed."
    )

async def setup(bot):
await bot.add_cog(
Management(bot)
)