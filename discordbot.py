import discord
from base64 import decode
import os
from discord.ext import commands, tasks
from var import *
import asyncio

bot = commands.Bot(command_prefix=prefix, description=description,intents = intents)

# Reload extension
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    extension = extension.lower()
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    print(f'Reloaded {extension}')
    await ctx.send(f':gear: Reloaded {extension}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.ExtensionNotLoaded):
        print(':no_entry: Extension not loaded')
    elif isinstance(error, commands.ExtensionAlreadyLoaded):
        print(':no_entry: Extension already loaded')

#Imports COG files
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

print (discord.opus.is_loaded())
bot.run(token)