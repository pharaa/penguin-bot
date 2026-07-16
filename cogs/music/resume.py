import discord
from discord.ext import commands

class Resume(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @discord.app_commands.command(name="resume", description="Возобновить воспроизведение")
    async def resume(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client

        if voice_client is None:
            return await interaction.response.send_message("Бот не в канале")

        if not voice_client.is_paused():
            return await interaction.response.send_message("Музыка не на паузе")

        voice_client.resume()
        await interaction.response.send_message("Воспроизведение возобновлено")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Resume(bot))