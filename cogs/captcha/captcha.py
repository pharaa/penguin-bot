import discord
from discord.ext import commands
from discord.ui import Button, View

class VerifButton(View):
    def __init__(self):
        super().__init__(persistent=False)
        self.ROLE_ID = 1526509836777426994
        
    @discord.ui.button(label="Верифицировать", style=discord.ButtonStyle.green)
    async def role(self, interaction: discord.Interaction, button: Button):
        role = interaction.guild.get_role(self.ROLE_ID)
        
        await interaction.user.add_roles(role)
        await interaction.response.send_message("Проверка пройдена чувак", ephemeral=True)

class Captcha(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.embed = discord.Embed(
            title="Верификация",
            description="Нажмите кнопку ниже чтобы получить доступ к серверу."
        )
        
    @discord.app_commands.command(name="init", description="Отправка всего нужного кала от имени бота")
    @commands.has_permissions(administrator=True)
    async def init(self, interaction: discord.Interaction, role: discord.Role):
        channel = self.bot.get_channel(1526519348137689168)
        await channel.send(embed=self.embed, view=VerifButton(role.id))
        await interaction.message.delete()
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Captcha(bot))