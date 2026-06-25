import discord
from discord.ext import commands
from discord import app_commands
import random


class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def generate_response(self, prompt: str):
        prompt = prompt.lower()

        # simple keyword-based responses
        if "hello" in prompt or "hi" in prompt:
            return random.choice([
                "Hey!",
                "Hello there!",
                "Hi 👋",
                "Yo!"
            ])

        if "how are you" in prompt:
            return random.choice([
                "I'm just code, but I'm doing fine!",
                "All systems running smoothly.",
                "I'm good 👍"
            ])

        if "help" in prompt:
            return "Try using /ask or mention me for quick replies."

        if "joke" in prompt:
            return random.choice([
                "Why did the computer crash? It had too many tabs open.",
                "I'm not lazy, I'm on energy-saving mode.",
                "Why do programmers hate nature? Too many bugs."
            ])

        if "who are you" in prompt:
            return "I'm your Discord bot assistant 🤖"

        return random.choice([
            "I'm not sure about that.",
            "Interesting question.",
            "Can you explain more?",
            "I don't know that yet."
        ])

    # ---------------- /ask COMMAND ----------------
    @app_commands.command(
        name="ask",
        description="Ask the AI something"
    )
    async def ask(
        self,
        interaction: discord.Interaction,
        question: str
    ):
        response = self.generate_response(question)

        await interaction.response.send_message(
            f"🤖 **You:** {question}\n💬 **AI:** {response}"
        )

    # ---------------- CHAT TRIGGER ----------------
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user.mentioned_in(message):
            response = self.generate_response(message.content)

            await message.reply(response)


async def setup(bot):
    await bot.add_cog(AI(bot))