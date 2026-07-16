import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"i can see you")
    
async def main():
    await bot.load_extension("cogs.music.play")
    await bot.load_extension("cogs.music.pause")
    await bot.load_extension("cogs.music.resume")
    await bot.load_extension("cogs.music.skip")
    
@bot.event
async def on_message(message: discord.Message):
    channel = bot.get_channel(1526268342749368330)
    
    if message.channel == channel:
        await message.delete()
        await message.author.ban(reason="Mrbeast where is my money")
    else:
        pass
    await bot.process_commands(message)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    
    with open("token.txt", 'r') as file:
        token = file.read()
        bot.run(token)