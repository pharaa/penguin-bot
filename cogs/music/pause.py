import discord
from discord.ext import commands

class Pause(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @discord.app_commands.command(name="pause", description="Поставить на паузу")
    async def pause(interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client

        if voice_client is None:
            return await interaction.response.send_message("Бот не в канале")

        if not voice_client.is_playing():
            return await interaction.response.send_message("Сейчас ничего не играет")

        voice_client.pause()
        await interaction.response.send_message("Поставил на паузу")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Pause(bot))