import discord
from discord.ext import commands
from discord import app_commands
import os
import sys

ALLOWED_USER_ID = 123456789012345678 # айди тех кто может перезапускать бота

class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
@discord.app_commands.command(name="restart", description="Перезапустить бота")
    async def restart_bot(self, interaction: discord.Interaction):
        if interaction.user.id != ALLOWED_USER_ID:
            await interaction.response.send_message("У вас нет прав для перезапуска бота.", ephemeral=True)
            return

        await interaction.response.send_message("Перезапуск", ephemeral=True)
        
        await self.bot.close()
        sys.exit(0)

async def setup(bot):
    await bot.add_cog(Restart(bot))
