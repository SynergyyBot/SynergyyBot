import discord
from discord.ext import commands, tasks, timers
import random
import datetime
import asyncio

timescales = ['sec', 'seconds', 'min', 'mins', 'minute', 'minutes', 'hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months', 'year'] # right now only supports up to week
client = commands.Bot(command_prefix='!')
client.remove_command("help")

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

@client.command(pass_context=True) # Custom Help Command
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.green(),
    )

    embed.set_author(name='Help', icon_url="https://cdn.discordapp.com/attachments/717853456244670509/718935942605439006/Screen_Shot_2020-06-06_at_5.14.29_PM.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/717853456244670509/718950987762761758/SynergyyNoBg.png")
    embed.add_field(name='!ping', value = 'Returns the bot\'s latency.', inline=False)
    embed.add_field(name='!clear (# of messages)', value = 'Clears messages from the current channel.\n    eg. !clear 10', inline=False)
    embed.add_field(name='!meeting', value = 'Creates a new meeting.\n    eg. !meeting Physics Project in 2 hours', inline=False)
    embed.add_field(name='-------------------------------------', value = "Visit our [website](https://www.filler.com/) for more help!", inline=False)
    embed.set_footer(text="All commands can be invoked using !")

    await ctx.send(embed=embed)

@client.command() #Meeting Creation Command
async def meeting(ctx, *, information):
    error_card = discord.Embed(title='Missing Meeting Time', colour=discord.Color.green())
    info = information.strip().split()
    for i in range(len(info)):
        for j in range(len(timescales)):
            #If user requests a meeting 'IN' a certain amount of time
            if timescales[j] in info[i] and i > 1 and info[i-1].isnumeric():
                name = information[:information.index(info[i-1])] if info[i-2] != 'in' else information[:information.rindex(' in ')]
                now = datetime.datetime.now().timestamp()
                m_time = 0
                if j == 0 or j == 1:
                    m_time = now + int(info[i-1])
                elif j == 2 or j == 3:
                    m_time = now + int(info[i-1]) * 60
                elif j == 4:
                    m_time = now + int(info[i-1]) * 3600
                elif j == 5:
                    m_time = now + int(info[i-1]) * 86400
                elif j == 6:
                    m_time = now + int(info[i-1]) * 604800
                time = datetime.datetime.fromtimestamp(m_time).strftime('%-I:%M%p')
                date = datetime.datetime.fromtimestamp(m_time).strftime('%A, %b %-d, %Y')

                #Create embed
                meeting_card = discord.Embed(title=f"\U0001F5D3 Meeting Created: {name}", colour=discord.Colour.green())
                meeting_card.add_field(name="Meeting Time", value=f"{time} on {date}")
                meeting_card.set_footer(text=f"Tip: I will remind you about this meeting when its starting!")
                await ctx.send(content=None, embed=meeting_card)

                await asyncio.sleep(m_time-now)
                reminder_card = discord.Embed(
                colour = discord.Colour.green(),
                )
                reminder_card.set_author(name="Hey! This is a reminder about your meeting, \"{0}\".\nHead over to your team's discord server to participate!".format(name))
                await ctx.author.send(content=None, embed=reminder_card)

                announce = discord.Embed(colour=discord.Colour.green())
                announce.set_author(name=f"\U00002755 Attention! The meeting \"{name}\" is starting now.")
                await ctx.send(embed=announce)


#Bot Token Pairing--------------------------------
client.run('TOKEN')