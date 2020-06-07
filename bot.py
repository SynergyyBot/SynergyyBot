import discord
from discord.ext import commands, tasks, timers
import random
import datetime

client = commands.Bot(command_prefix='!')

#On Ready Event------------------------------------------

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(" !help"))
    print('SynergyyBot is ready!')

#Commands-----------------------------------------

@client.command() #Ping Command
async def ping(ctx):
    await ctx.send(f'Pong! My current latency is {round(client.latency*1000)}ms.')

@client.command(pass_context=True) #Clear Messages Command
async def clear(ctx, amount=10):
    amount = int(amount)
    await ctx.channel.purge(limit=amount+1)  
    amount = str(amount)
    await ctx.send(":white_check_mark: "+amount+" messages cleared!", delete_after=5)

#Bot Token Pairing--------------------------------
client.run('TOKEN')