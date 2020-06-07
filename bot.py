import discord
import os
import datetime
import time
import threading
from discord.ext import commands, tasks
from word2number import w2n

client = commands.Bot(command_prefix='!')
timescales = ['sec', 'second', 'min', 'minute', 'hour', 'day', 'week', 'month', 'year'] # right now only supports up to week

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

@client.command()
async def meeting(ctx, *, information):
    error_card = discord.Embed(title='Missing Meeting Time', colour=discord.Color.green())
    info = information.strip().split()
    name = _time = date = ''

    for i in range(len(info)):
        for j in range(len(timescales)):
            #If user requests a meeting IN a certain amount of time
            if timescales[j] in info[i] and i > 1:
                if info[i-1].isnumeric():
                    t = int(info[i-1])
                else:
                    t = w2n.word_to_num(info[i-1])
                name = information[:information.index(info[i-1])] if info[i-2] != 'in' else information[:information.rindex(' in ')]
                now = datetime.datetime.now().timestamp()
                m_time = 0
                if j == 0 or j == 1:
                    m_time = now + t
                elif j == 2 or j == 3:
                    m_time = now + t * 60
                elif j == 4:
                    m_time = now + t * 3600
                elif j == 5:
                    m_time = now + t * 86400
                elif j == 6:
                    m_time = now + t * 604800
                _time = datetime.datetime.fromtimestamp(m_time).strftime('%-I:%M%p')
                date = datetime.datetime.fromtimestamp(m_time).strftime('%A, %b %-d, %Y')

                #Create embed
                meeting_card = discord.Embed(title=f"\U0001F5D3 Meeting Created: {name}", colour=discord.Colour.green())
                meeting_card.add_field(name="Meeting Time", value=f"{_time} on {date}")
                await ctx.send(content=None, embed=meeting_card)

#Client Token (removed for security reasons)
client.run('TOKEN')