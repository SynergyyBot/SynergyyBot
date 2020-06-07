import discord
import os
from discord.ext import commands, tasks

client = commands.Bot(command_prefix='!')

#On Ready--------------------------------

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)}ms')

@client.command()
async def clearmssg(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

#Client Token (removed for security reasons)
client.run('TOKEN')