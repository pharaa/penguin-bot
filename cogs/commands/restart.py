import discord
from discord.ext import commands
from discord import app_commands
import os
import sys

ALLOWED_USER_ID = 123456789012345678 # айди тех кто может перезапускать бота

class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="restart", description="Перезапустить бота")
    async def restart_bot(self, interaction: discord.Interaction):
        if interaction.user.id != ALLOWED_USER_ID:
            await interaction.response.send_message("У вас нет прав для перезапуска бота.", ephemeral=True)
            return

        await interaction.response.send_message("Бот уходит в рестарт... 🔄", ephemeral=True)

        os.execv(sys.executable, [sys.executable] + sys.argv)


async def setup(bot):
    await bot.add_cog(Restart(bot))