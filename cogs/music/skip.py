import discord
from discord.ext import commands

class Skip(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @discord.app_commands.command(name="skip", description="Скипнуть песню")
    async def skip(interaction: discord.Interaction):
        if interaction.guild.voice_client and (interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
            interaction.guild.voice_client.stop()
            await interaction.response.send_message("Песня скипнута")
        else:
            await interaction.response.send_message("Сейчас ничего не играет")
            
async def setup(bot: commands.Bot):
    await bot.add_cog(Skip(bot))