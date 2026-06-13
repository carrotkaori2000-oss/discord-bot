import discord
from discord.ext import commands
import os  
from dotenv import load_dotenv

intents = discord.Intents.all()
intents.message_content = True

load_dotenv()
bot = commands.Bot(command_prefix="$", intents = intents)

@bot.event
async def on_ready():
    for FileName in os.listdir('./cmds'):
        if FileName.endswith('.py'):
            print(f'loading cmds.{FileName[:-3]}')
            await bot.load_extension(f'cmds.{FileName[:-3]}')
    
    print(">>Bot is Online<<")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"【最外層大門】收到任何人發出的訊息了: {message.content}")
    await bot.process_commands(message) 

@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded')

@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'Reloaded')

@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Unloaded')

if  __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))
