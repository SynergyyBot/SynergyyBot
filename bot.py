import discord
import os
from discord.ext import commands, tasks

client = commands.Bot(command_prefix='!')

#On Ready--------------------------------

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#Client Token (removed for security reasons)
client.run('TOKEN')