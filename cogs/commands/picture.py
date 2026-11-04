import duckduckgo_search
import discord
from discord.ext import commands


class Pic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.ddgs = duckduckgo_search.DDGS()
        self.bot = bot

    @discord.app_commands.command(name="pic", description="Выдаёт картинку по запросу")
    async def clear(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer(ephemeral=True)
        results = self.ddgs.images(keywords=query)
        await interaction.followup.send(results[0]["image"])

async def setup(bot: commands.Bot):
    await bot.add_cog(Pic(bot))
