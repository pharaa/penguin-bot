import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ID = 1526268342749368330
GUILD_ID = 1496883454011248661

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    bot.tree.clear_commands(guild=None)
    try:
        await bot.tree.sync()
        print("Глобальные команды успешно стерты из Discord.")
    except Exception as e:
        print(f"Не удалось очистить глобальные команды: {e}")

    try:
        await bot.load_extension("cogs.music.play")
        await bot.load_extension("cogs.music.pause")
        await bot.load_extension("cogs.music.resume")
        await bot.load_extension("cogs.music.skip")
        print("Коги успешно загружены.")
    except discord.errors.ExtensionAlreadyLoaded:
        print("Коги уже были загружены.")

    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f"i can see you")
    
@bot.event
async def on_message(message: discord.Message):
    channel = bot.get_channel(CHANNEL_ID)
    
    if message.channel == channel:
        await message.delete()
        await message.author.ban(reason="Mrbeast where is my money")
    else:
        pass
    await bot.process_commands(message)

if __name__ == "__main__":
    with open("token.txt", 'r') as file:
        token = file.read()
        bot.run(token)
