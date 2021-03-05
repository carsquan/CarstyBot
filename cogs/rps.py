import discord
from discord.ext import commands

import random

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

async def messageUser(self, message, reciever):
    try:
        dm = discord.DMChannel()
        dm.recipient = reciever

        return await dm.send(message)
    except:
        print("ERROR in messageUser\n")
async def playRockPaperScissors(self, p1, p2,channel):
    if not await confirmation(self, f'<@!{p2.id}>! Do you want to play Rock Paper Scissors with {p1.display_name}?', p2, channel, cancelledMessage=':x: Rock Paper Scissors cancelled!', successMessage='Starting Rock Paper Scissors'):
        return
    


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
            playerTwo = await ctx.guild.fetch_member(int(user[3:-1]))

            await playRockPaperScissors(self, ctx.author, playerTwo, ctx.channel)
        except:
            await ctx.send(':no_entry: Player not found!')


    @rps.error
    async def rps_error(self, ctx, error):
        await ctx.send('Command format: `rpc [User]`')

def setup(client):
    client.add_cog(rps(client))