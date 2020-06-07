import discord
from discord.ext import commands, tasks, timers
import random
import datetime

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
    embed.add_field(name='!clear (# of messages)', value = 'Clears messages from the current channel.', inline=False)
    #embed.add_field(name='-------------------------------------', value = "Visit our [website](https://www.youtube.com/) for more help!", inline=False)
    embed.set_footer(text="All commands can be invoked using !")

    await ctx.send(embed=embed)

#Bot Token Pairing--------------------------------
client.run('TOKEN')