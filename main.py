import discord
from discord.ext import commands
import os
import asyncio
import logging

from views.ticket_views import TicketView
from views.giveaway_views import GiveawayView
from views.role_views import RoleView
from views.verification_views import VerificationView

# ---------------- TOKEN ----------------
TOKEN = os.getenv("TOKEN")

# ---------------- INTENTS ----------------
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

# ---------------- LOGS FOLDER ----------------
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

        self.owner_id = 1275009250405519391

    async def setup_hook(self):
        print("Loading cogs...")

        # ---------------- LOAD COGS ----------------
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{file[:-3]}")
                    print(f"Loaded cog: {file}")
                except Exception as e:
                    print(f"Failed cog {file}: {e}")

        # ---------------- LOAD EVENTS ----------------
        if os.path.exists("./events"):
            print("Loading events...")
            for file in os.listdir("./events"):
                if file.endswith(".py"):
                    try:
                        await self.load_extension(f"events.{file[:-3]}")
                        print(f"Loaded event: {file}")
                    except Exception as e:
                        print(f"Failed event {file}: {e}")

        # ---------------- REGISTER VIEWS (IMPORTANT) ----------------
        self.add_view(TicketView())
        self.add_view(GiveawayView())
        self.add_view(RoleView())
        self.add_view(VerificationView())

        # ---------------- SYNC SLASH COMMANDS ----------------
        try:
            await self.tree.sync()
            print("Slash commands synced.")
        except Exception as e:
            print(f"Sync error: {e}")

    async def on_ready(self):
        print(f"Logged in as {self.user}")

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name="/help")
        )

    # ---------------- ERROR HANDLING ----------------
    async def on_command_error(self, ctx, error):
        logging.error(f"Prefix error: {error}")

    async def on_app_command_error(self, interaction, error):
        logging.error(f"Slash error: {error}")

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