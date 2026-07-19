import discord
from discord.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):

        deleted = await ctx.channel.purge(limit=amount + 1)


        await ctx.send(f'Удалено {len(deleted) - 1} сообщений.', delete_after=3.0)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Укажи количество сообщений для удаления (например: !clear 10)", delete_after=3.0)
        elif isinstance(error, commands.MissingPermissions):
            pass


async def setup(bot):
    await bot.add_cog(Clear(bot))