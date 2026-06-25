import discord
from discord.ext import commands
import os
import asyncio
import logging

# ---------------- TOKEN ----------------
TOKEN = os.getenv("TOKEN")

# ---------------- INTENTS ----------------
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

# ---------------- LOGGING SETUP ----------------
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(name)s: %(message)s"
)

error_logger = logging.getLogger("discord.errors")


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

        self.owner_id = 1275009250405519391

    # ---------------- LOAD EVERYTHING ----------------
    async def setup_hook(self):
        print("Loading cogs...")

        # LOAD COGS
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{file[:-3]}")
                    print(f"Loaded cog: {file}")
                except Exception as e:
                    print(f"Failed cog {file}: {e}")

        # LOAD EVENTS
        if os.path.exists("./events"):
            print("Loading events...")
            for file in os.listdir("./events"):
                if file.endswith(".py"):
                    try:
                        await self.load_extension(f"events.{file[:-3]}")
                        print(f"Loaded event: {file}")
                    except Exception as e:
                        print(f"Failed event {file}: {e}")

        # SYNC SLASH COMMANDS
        try:
            await self.tree.sync()
            print("Slash commands synced.")
        except Exception as e:
            print(f"Sync error: {e}")

    # ---------------- READY ----------------
    async def on_ready(self):
        print(f"Logged in as {self.user}")

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name="/help")
        )

    # ---------------- ERROR HANDLING ----------------
    async def on_command_error(self, ctx, error):
        logging.error(f"Command error: {error}")

    async def on_app_command_error(self, interaction, error):
        logging.error(f"Slash command error: {error}")

        try:
            if interaction.response.is_done():
                await interaction.followup.send("❌ An error occurred.")
            else:
                await interaction.response.send_message("❌ An error occurred.")
        except:
            pass


# ---------------- START BOT ----------------
bot = Bot()


async def main():
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())