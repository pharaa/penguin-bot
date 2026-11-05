from io import BytesIO
from random import choice

import aiohttp
import discord
from discord.ext import commands


class Pic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="pic", description="Выдаёт картинку по запросу")
    async def clear(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer(ephemeral=False)
        if not self.bot.search_api_key:
            await interaction.followup.send("Поиск картинок не настроен.", ephemeral=True)
            return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://serpapi.com/search.json",
                    params={"engine": "google_images", "q": query, "safe": "off", "api_key": self.bot.search_api_key},
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                images = [item["thumbnail"] for item in data.get("images_results", []) if item.get("thumbnail", "").startswith("https://")]
                if not images:
                    await interaction.followup.send("Картинки не найдены.", ephemeral=True)
                    return
                async with session.get(choice(images), timeout=aiohttp.ClientTimeout(total=15)) as response:
                    response.raise_for_status()
                    content = await response.read()
        except (aiohttp.ClientError, TimeoutError):
            await interaction.followup.send("Не удалось выполнить поиск картинок.", ephemeral=True)
            return
        await interaction.followup.send(file=discord.File(BytesIO(content), filename="image.jpg"))


async def setup(bot: commands.Bot):
    await bot.add_cog(Pic(bot))
