import discord
from discord.ext import commands
from events._base import get_log_channel_obj

class VoiceEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        channel = await get_log_channel_obj(member.guild)

        if not channel:
            return

        if before.channel is None and after.channel:
            await channel.send(f"🔊 {member} joined {after.channel.name}")

        elif before.channel and not after.channel:
            await channel.send(f"🔇 {member} left voice")

        elif before.channel != after.channel:
            await channel.send(f"🔁 {member} moved voice channels")

async def setup(bot):
    await bot.add_cog(VoiceEvents(bot))