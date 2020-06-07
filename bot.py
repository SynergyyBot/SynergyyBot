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

@client.command()
async def helpme(ctx):
    card = discord.Embed(title="Bot Help", description="Below are some useful commands", colour=discord.Colour.green())
    card.add_field(name="!ping", value="Returns the latency of the bot")
    card.add_field(name="!clearmmsg n", value="Clears previous n messages")
    await ctx.send(content=None, embed=card)

#Client Token (removed for security reasons)
client.run('TOKEN')