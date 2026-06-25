from discord.ext import commands
from discord import app_commands
import discord

class Help(commands.Cog):
def init(self, bot):
self.bot = bot

@app_commands.command(
    name="help",
    description="Shows all available commands"
)
async def help(
    self,
    interaction: discord.Interaction
):
    embed = discord.Embed(
        title="🤖 Bot Commands",
        description="Use the categories below to find commands.",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="🛡 Moderation",
        value="""

/ban
/kick
/timeout
/warn
/clear
""",
inline=False
)

    embed.add_field(
        name="⚙ Management",
        value="""

/lock
/unlock
/slowmode
/createchannel
/createrole
""",
inline=False
)

    embed.add_field(
        name="🎮 Fun",
        value="""

/coinflip
/dice
/rps
""",
inline=False
)

    embed.add_field(
        name="🛠 Utility",
        value="""

/ping
/avatar
/userinfo
/serverinfo
""",
inline=False
)

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )

async def setup(bot):
await bot.add_cog(Help(bot))