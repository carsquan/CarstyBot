import discord
from base64 import decode
import os
from discord.ext import commands, tasks
from var import *




#Var includes token variable
bot = commands.Bot(command_prefix=prefix, description=description, intents = intents)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
bot.run(token)