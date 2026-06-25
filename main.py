import discord
from discord.ext import commands
import asyncio
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

EXTENSIONS = [
    "cogs.moderation",
    "cogs.setup"
]

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    print(f"Logged in as {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print("------------------------")

async def load_extensions():
    for extension in EXTENSIONS:
        try:
            await bot.load_extension(extension)
            print(f"Loaded: {extension}")
        except Exception as e:
            print(f"Failed to load {extension}: {e}")

async def main():
    if not TOKEN:
        raise ValueError("TOKEN environment variable is missing")

    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
