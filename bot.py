import discord
import os
import datetime
import time
import threading
import asyncio
from discord.ext import commands, tasks
from word2number import w2n
from dateutil.parser import parse

client = commands.Bot(command_prefix='!')
timescales = ['sec', 'second', 'min', 'minute', 'hour', 'day', 'week', 'month', 'year'] # right now only supports up to week

#On Ready--------------------------------

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#Commands----------------------------------

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
    time_missing = discord.Embed(title='Missing Meeting Time!', colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description='Please put the name in quotations:\neg. !meeting \"Physics Project\" in 2 hours', colour=discord.Color.green())
    info = information.strip().split()
    name = time = date = ''
    in_condition = True

    for i in range(len(info)):
        for j in range(len(timescales)):
            #If user requests a meeting IN a certain amount of time
            if timescales[j] in info[i].lower() and i >= 1:
                in_condition = False

                #(!meeting name in # timescale)
                if info[i-1].isnumeric():
                    t = int(info[i-1])
                    name = information[:information.index(info[i-1])] if info[i-2] != 'in' else information[:information.rindex(' in ')]
                #(!meeting name in #timescale)
                elif info[i].lower()[:info[i].lower().index(timescales[j])].isnumeric():
                    t = int(info[i].lower()[:info[i].lower().index(timescales[j])])
                    name = information[:information.index(info[i])] if info[i-1] != 'in' else information[:information.rindex(' in ')]
                #(!meeting name in word# timescale)
                else:
                    t = w2n.word_to_num(info[i-1])
                    name = information[:information.index(info[i-1])] if info[i-2] != 'in' else information[:information.rindex(' in ')]
                
                name = name.strip('\"')
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
                time = datetime.datetime.fromtimestamp(m_time).strftime('%-I:%M%p')
                date = datetime.datetime.fromtimestamp(m_time).strftime('%A, %b %-d, %Y')

                #Create embed
                meeting_card = discord.Embed(title=f"\U0001F5D3 Meeting Created: {name}", colour=discord.Colour.green())
                meeting_card.add_field(name="Meeting Time", value=f"{time} on {date}")
                await ctx.send(content=None, embed=meeting_card)
    
    if in_condition:
        if '\"' in information:
            name = information[information.index('\"')+1 : information.rindex('\"')]
            if has_date(information[information.rindex('\"')+1:]):
                d = parse(information[information.rindex('\"')+1:])
                time = d.strftime('%-I:%M%p')
                date = d.strftime('%A, %b %-d, %Y')

                #Create embed
                meeting_card = discord.Embed(title=f"\U0001F5D3 Meeting Created: {name}", name="Meeting Time", value=f"{time} on {date}", colour=discord.Colour.green())
                await ctx.send(content=None, embed=meeting_card)
            else:
                await ctx.send(content=None, embed=time_missing)
        else:
            await ctx.send(content=None, embed=format_error)


#Other Functions--------------------------

def has_date(string, fuzzy=True):
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

#Error Handling----------------------------

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        command_not_found = discord.Embed(title="Command Not Found", description="Use !helpme to see the list of commands.", colour=discord.Colour.green())
        await ctx.send(content=None, embed=command_not_found)

#Meeting Error------------------------------------
@meeting.error
async def meeting_error(ctx, error):
    time_missing = discord.Embed(title='Missing Meeting Time!', colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description='Please put the name in quotations:\neg. !meeting \"Physics Project\" in 2 hours', colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=time_missing)
    else:
        await ctx.send(content=None, embed=format_error)


#Client Token (removed for security reasons)
client.run('NzE3NDMyMzc0OTY2ODc4MjM4.Xt_qqA.vMqd06AhGLI-xa8H3iaDGX5k7Tk')