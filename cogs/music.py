import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import yt_dlp

ytdl_format_options = {
    'format': 'bestaudio/best',
    'quiet': True,
    'noplaylist': True
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

queues = {}


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_queue(self, guild_id):
        return queues.setdefault(guild_id, [])

    async def play_next(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        queue = self.get_queue(guild_id)

        if len(queue) == 0:
            return

        url, title = queue.pop(0)

        voice_client = interaction.guild.voice_client

        if not voice_client:
            return

        source = discord.FFmpegPCMAudio(url, **ffmpeg_options)

        def after_playing(error):
            fut = asyncio.run_coroutine_threadsafe(
                self.play_next(interaction),
                self.bot.loop
            )
            try:
                fut.result()
            except:
                pass

        voice_client.play(source, after=after_playing)

    # ---------------- JOIN ----------------
    @app_commands.command(
        name="join",
        description="Join your voice channel"
    )
    async def join(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            return await interaction.response.send_message(
                "❌ You are not in a voice channel."
            )

        channel = interaction.user.voice.channel

        await channel.connect()

        await interaction.response.send_message(
            f"🔊 Joined {channel.name}"
        )

    # ---------------- PLAY ----------------
    @app_commands.command(
        name="play",
        description="Play a song from YouTube URL"
    )
    async def play(
        self,
        interaction: discord.Interaction,
        url: str
    ):
        await interaction.response.defer()

        if not interaction.user.voice:
            return await interaction.followup.send(
                "❌ Join a voice channel first."
            )

        voice_channel = interaction.user.voice.channel
        voice_client = interaction.guild.voice_client

        if not voice_client:
            voice_client = await voice_channel.connect()

        info = ytdl.extract_info(url, download=False)
        title = info.get("title", "Unknown")

        stream_url = info["url"]

        queue = self.get_queue(interaction.guild.id)
        queue.append((stream_url, title))

        if not voice_client.is_playing():
            await self.play_next(interaction)

        await interaction.followup.send(
            f"🎶 Added to queue: **{title}**"
        )

    # ---------------- SKIP ----------------
    @app_commands.command(
        name="skip",
        description="Skip current song"
    )
    async def skip(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client

        if not vc or not vc.is_playing():
            return await interaction.response.send_message(
                "❌ Nothing is playing."
            )

        vc.stop()

        await interaction.response.send_message(
            "⏭ Skipped."
        )

    # ---------------- LEAVE ----------------
    @app_commands.command(
        name="leave",
        description="Leave voice channel"
    )
    async def leave(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client

        if not vc:
            return await interaction.response.send_message(
                "❌ I'm not in a voice channel."
            )

        await vc.disconnect()

        await interaction.response.send_message(
            "👋 Left voice channel."
        )


async def setup(bot):
    await bot.add_cog(Music(bot))