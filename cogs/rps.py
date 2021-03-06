import discord
from discord import message
from discord.ext import commands

import random

async def checkWinner(p1,p2):
    if ((p1 == 0 and p2 == 1) or (p1 == 1 and p2 == 2 ) or (p1 == 2 and p2 == 0)):
        return 2
    elif ((p1 == 1 and p2 == 0) or (p1==2 and p2 == 1) or (p1 ==0 and p2 == 2)):
        return 1
    return 0
async def confirmation(self, message, sentUser, channel, successMessage = ':white_check_mark: Operation successful', cancelledMessage = ':x: Operation cancelled'):
    new_message = await channel.send(message)

    await new_message.add_reaction('✅')
    await new_message.add_reaction('❌')

    def check(reaction, user):
        return user == sentUser

    reaction = None

    while True:
        if str(reaction) == '✅':
            await new_message.clear_reactions()
            await new_message.edit(content=successMessage)
            return True
        elif str(reaction) == '❌':
            await new_message.clear_reactions()
            await new_message.edit(content=cancelledMessage)
            return False

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout = 30.0, check = check)
            await new_message.remove_reaction(reaction, user)
        except:
            await new_message.clear_reactions()
            await new_message.edit(content=cancelledMessage)
            return False

async def rpsChoice(self, sentUser):
    
    message = "Whats your choice"
    new_message = await sentUser.send(message)

    await new_message.add_reaction('🔥')
    await new_message.add_reaction('💧')
    await new_message.add_reaction('🌲')

    def check(reaction, user):
        return user == sentUser

    reaction = None

    while True:
        print(reaction)
        if str(reaction) == '🔥':
            await sentUser.send(content="You have chosen fire")
            print(f"{sentUser.id} chose fire")
            return 0
        elif str(reaction) == '💧':
            await sentUser.send(content="You have chosen water")
            print(f"{sentUser.id} chose water")
            return 1
        elif str(reaction) == '🌲':
            await sentUser.send(content="You have chosen grass")
            print(f"{sentUser.id} chose grass")
            return 2

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout = 30.0, check = check)
        except:
            await sentUser.send(content="You have run out of time(sad)")
            return



async def messageUser(self, message, reciever):
    try:

        return await reciever.send(message)
    except:
        print("ERROR in messageUser\n")


async def playRockPaperScissors(self, p1, p2,channel):
    try:
        if not await confirmation(self, f'<@!{p2.id}>! Do you want to play Rock Paper Scissors with {p1.display_name}?', p2, channel, cancelledMessage=':x: Rock Paper Scissors cancelled!', successMessage='Starting Rock Paper Scissors'):
            return
        p1Choice = await rpsChoice(self,sentUser = p1)
        p2Choice = await rpsChoice(self,sentUser = p2)
        switcher = {
            0: "Draw",
            1: f"<@!{p1.id}> won!",
            2: f"<@!{p2.id}> won!",
        }
        msg = switcher.get(await checkWinner(p1Choice,p2Choice),"Error or Someone times out smh")
        return await channel.send(msg)
    except Exception as e: print(e)


class rps(commands.Cog):
    """Rolling of the die"""
    def __init__(self, client):
        self.client = client

    

    @commands.Cog.listener()
    async def on_ready(self):
        className = "Rock Paper Scissors"
        print(f'{className} loaded...')

    @commands.command()
    async def rps(self, ctx, user:str):
        #Rock Paper Scissors

        print(f'{ctx.author} has challenged {user} to Rock Paper Scissors')
        try:
            p2id = int(user[3:-1])
            playerTwo = await ctx.guild.fetch_member(p2id)
            
            await playRockPaperScissors(self, ctx.author, playerTwo, ctx.channel)
        except:
            await ctx.send(':no_entry: Player not found!')


    @rps.error
    async def rps_error(self, ctx, error):
        await ctx.send('Command format: `rpc [User]`')

def setup(client):
    client.add_cog(rps(client))