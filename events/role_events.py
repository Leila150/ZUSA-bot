import discord
from discord.ext import commands

class RoleEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        channel = discord.utils.get(after.guild.text_channels, name="logs")

        if not channel:
            return

        before_roles = set(before.roles)
        after_roles = set(after.roles)

        added = after_roles - before_roles
        removed = before_roles - after_roles

        for role in added:
            if role.name != "@everyone":
                await channel.send(f"➕ {after} got {role.name}")

        for role in removed:
            if role.name != "@everyone":
                await channel.send(f"➖ {after} lost {role.name}")

async def setup(bot):
    await bot.add_cog(RoleEvents(bot))