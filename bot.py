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

#Error Handling----------------------------

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        command_not_found = discord.Embed(title="Command Not Found :(", description="Use !help to see the list of commands and how to use them.", colour=discord.Colour.green())
        await ctx.send(content=None, embed=command_not_found)

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

@client.command() #Coinflip Command
async def flip(ctx):
    choices = ["Heads", "Tails"]
    rancoin = random.choice(choices)
    coinflip_card = discord.Embed(colour = discord.Colour.green(), description=f"The result was **{rancoin}**!")
    await ctx.send(embed=coinflip_card)

@client.command(aliases=['8ball']) #8ball Command
async def _8ball(ctx, *, question):
    responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.",
                "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.",
                "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
                "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
    _8ball_card = discord.Embed(colour = discord.Colour.green(), description = f"**Question:** {question}\n**Answer:** {random.choice(responses)}")
    await ctx.send(embed=_8ball_card)

@_8ball.error
async def _8ball_error(ctx, error):
    arg_missing = discord.Embed(title='Missing Required Argument!', description="You need to ask the 8ball a question!\neg. !8ball Am I cool?\n Please refer to !help for more info.", colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description="Please follow this format: !8ball Am I cool?\n Please refer to !help for more info.", colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=arg_missing)
    else:
        await ctx.send(content=None, embed=format_error)

@client.command(pass_context=True) # Custom Help Command
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.green(),
    )
    embed.set_author(name='Help', icon_url="https://cdn.discordapp.com/attachments/717853456244670509/718935942605439006/Screen_Shot_2020-06-06_at_5.14.29_PM.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/717853456244670509/718950987762761758/SynergyyNoBg.png")
    embed.add_field(name='!meeting', value = 'Creates a new meeting.\neg. !meeting Physics Project in 2 hours', inline=False)
    embed.add_field(name='!clear (# of messages)', value = 'Clears messages from the current channel.\neg. !clear 10\nNote: If no number is provided, 10 is the default value.', inline=False)
    embed.add_field(name='!ping', value = 'Returns the bot\'s latency.', inline=False)
    embed.add_field(name='!flip', value = 'Flips a coin!', inline=False)
    embed.add_field(name='!8ball', value = 'Asks the magical 8ball for an answer to your question.\neg. !8ball Will I become succesful?', inline=False)
    embed.set_footer(text="Tip: All commands can be invoked using !")

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

@meeting.error
async def meeting_error(ctx, error):
    time_missing = discord.Embed(title='Missing Meeting Time!', description="For further help, please refer to !help", colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description='Please put the name in quotations:\neg. !meeting "Physics Project" in 2 hours', colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=time_missing)
    else:
        await ctx.send(content=None, embed=format_error)

#Poll Commands----------------------------------------------------------------
@client.command()
async def poll2(ctx, title, option1, option2, polltimeinminutes: int):

    options = {"🇦": option1,
                   "🇧": option2}
    vote = discord.Embed(title=f"\U0001F4F6 {title}", color=discord.Colour.green())
    value = "\n".join("{} - {}".format(*item) for item in options.items())
    vote.add_field(name="Options:", value=value, inline=False)
    vote.set_footer(text="Time to vote: %s minutes.\nUse the reactions below to vote." % (polltimeinminutes))

    message_1 = await ctx.send(embed=vote)
    for choice in options:
        await message_1.add_reaction(emoji=choice)

    polltimeinminutes *= 60
    await asyncio.sleep(polltimeinminutes)
    message_1 = await ctx.fetch_message(message_1.id)

    counts = {react.emoji: react.count for react in message_1.reactions}
    winner = max(options, key=counts.get)

    winner_card = discord.Embed(color=discord.Colour.green(), description= "\U00002B50 The winner of the poll **%s** is **%s**!" % (title, options[winner]))

    await ctx.send(embed=winner_card)

@client.command()
async def poll3(ctx, title, option1, option2, option3, polltimeinminutes: int):

    options = {"🇦": option1,
                   "🇧": option2,
                   "🇨": option3}
    vote = discord.Embed(title=f"\U0001F4F6 {title}", color=discord.Colour.green())
    value = "\n".join("{} - {}".format(*item) for item in options.items())
    vote.add_field(name="Options:", value=value, inline=False)
    vote.set_footer(text="Time to vote: %s minutes.\nUse the reactions below to vote." % (polltimeinminutes)) 

    message_1 = await ctx.send(embed=vote)
    for choice in options:
        await message_1.add_reaction(emoji=choice)

    polltimeinminutes *= 60
    await asyncio.sleep(polltimeinminutes)
    message_1 = await ctx.fetch_message(message_1.id)

    counts = {react.emoji: react.count for react in message_1.reactions}
    winner = max(options, key=counts.get)

    winner_card = discord.Embed(color=discord.Colour.green(), description= "\U00002B50 The winner of the poll **%s** is **%s**!" % (title, options[winner]))

    await ctx.send(embed=winner_card)

@client.command()
async def poll4(ctx, title, option1, option2, option3, option4, polltimeinminutes: int):

    options = {"🇦": option1,
                   "🇧": option2,
                   "🇨": option3, "🇩": option4}
    vote = discord.Embed(title=f"\U0001F4F6 {title}", color=discord.Colour.green())
    value = "\n".join("{} - {}".format(*item) for item in options.items())
    vote.add_field(name="Options:", value=value, inline=False)
    vote.set_footer(text="Time to vote: %s minutes.\nUse the reactions below to vote." % (polltimeinminutes)) # You can delete this line if you want.

    message_1 = await ctx.send(embed=vote)
    for choice in options:
        await message_1.add_reaction(emoji=choice)

    polltimeinminutes *= 60
    await asyncio.sleep(polltimeinminutes)
    message_1 = await ctx.fetch_message(message_1.id)

    counts = {react.emoji: react.count for react in message_1.reactions}
    winner = max(options, key=counts.get)

    winner_card = discord.Embed(color=discord.Colour.green(), description= "\U00002B50 The winner of the poll **%s** is **%s**!" % (title, options[winner])) 

    await ctx.send(embed=winner_card)

@client.command()
async def poll5(ctx, title, option1, option2, option3, option4, option5, polltimeinminutes: int):

    options = {"🇦": option1,
                   "🇧": option2,
                   "🇨": option3, "🇩": option4, "🇪": option5}
    vote = discord.Embed(title=f"\U0001F4F6 {title}", color=discord.Colour.green())
    value = "\n".join("{} - {}".format(*item) for item in options.items())
    vote.add_field(name="Options:", value=value, inline=False)
    vote.set_footer(text="Time to vote: %s minutes.\nUse the reactions below to vote." % (polltimeinminutes))

    message_1 = await ctx.send(embed=vote)
    for choice in options:
        await message_1.add_reaction(emoji=choice) 

    polltimeinminutes *= 60
    await asyncio.sleep(polltimeinminutes)
    message_1 = await ctx.fetch_message(message_1.id)

    counts = {react.emoji: react.count for react in message_1.reactions}
    winner = max(options, key=counts.get)

    winner_card = discord.Embed(color=discord.Colour.green(), description= "\U00002B50 The winner of the poll **%s** is **%s**!" % (title, options[winner]))

    await ctx.send(embed=winner_card)

#Poll Error Handling----------------------------

@poll2.error
async def poll2_error(ctx, error):
    arg_missing = discord.Embed(title='Missing Required Argument!', description="Please follow this format: !poll2 \"Title\" option1 option2 1\n Please refer to !help for more info.", colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description="Please follow this format: !poll2 \"Title\" option1 option2 1\n Please refer to !help for more info.", colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=arg_missing)
    else:
        await ctx.send(content=None, embed=format_error)

@poll3.error
async def poll3_error(ctx, error):
    arg_missing = discord.Embed(title='Missing Required Argument!', description="Please follow this format: !poll3 \"Title\" option1 option2 option3 1\n Please refer to !help for more info.", colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description="Please follow this format: !poll3 \"Title\" option1 option2 option3 1\n Please refer to !help for more info.", colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=arg_missing)
    else:
        await ctx.send(content=None, embed=format_error)

@poll4.error
async def poll4_error(ctx, error):
    arg_missing = discord.Embed(title='Missing Required Argument!', description="Please follow this format: !poll4 \"Title\" option1 option2 option3 option4 1\n Please refer to !help for more info.", colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description="Please follow this format: !poll4 \"Title\" option1 option2 option3 option4 1\n Please refer to !help for more info.", colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=arg_missing)
    else:
        await ctx.send(content=None, embed=format_error)

@poll5.error
async def poll5_error(ctx, error):
    arg_missing = discord.Embed(title='Missing Required Argument!', description="Please follow this format: !poll5 \"Title\" option1 option2 option3 option4 option5 1\n Please refer to !help for more info.", colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description="Please follow this format: !poll5 \"Title\" option1 option2 option3 option4 option5 1\n Please refer to !help for more info.", colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=arg_missing)
    else:
        await ctx.send(content=None, embed=format_error)

#Bot Token Pairing--------------------------------
client.run('TOKEN')