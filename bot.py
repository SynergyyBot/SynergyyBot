import discord
import os
from discord.ext import commands, tasks, timers
import random
import datetime
import time
import asyncio
from word2number import w2n
from dateutil.parser import parse

timescales = ['sec', 'second', 'min', 'minute', 'hour', 'day', 'week', 'month', 'year'] # right now only supports up to week
unicode_block = ['🇦','🇧','🇨','🇩','🇪','🇫','🇬','🇭','🇮','🇯','🇰','🇱','🇲','🇳','🇴','🇵','🇶','🇷','🇸','🇹','🇺','🇻','🇼','🇽','🇾','🇿']

client = commands.Bot(command_prefix='!')
client.timer_manager = timers.TimerManager(client)
client.remove_command("help")

#On Ready Event------------------------------------------

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(" !help"))
    print('Logged in as: {0.user}'.format(client))

#General Error Handling----------------------------------

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        command_not_found = discord.Embed(title="Command Not Found :(", description="Use !help to see the list of commands and how to use them.", colour=discord.Colour.green())
        await ctx.send(content=None, embed=command_not_found)

#Commands-------------------------------------------------

@client.command() #Ping Command
async def ping(ctx):
    await ctx.send(f'Pong! My current latency is {round(client.latency*1000)}ms.')

@client.command(pass_context=True) #Clear Messages Command
async def clear(ctx, amount=None):
    if amount.isnumeric():           
        amount = int(amount)
        await ctx.channel.purge(limit=amount+1)  
        amount = str(amount)
        await ctx.send(":white_check_mark: "+amount+" messages cleared!", delete_after=5)
    else:
        nonnumeric_card = discord.Embed(title="Error!", description="The value after !clear must be a number.\neg. !clear 50\nPlease refer to !help for more info.", colour=discord.Colour.green())
        await ctx.send(embed=nonnumeric_card)


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


@client.command
async def pog(ctx):
    pog_card = discord.Embed(colour = discord.Colour.green())
    pog_card.set_image(url="https://cdn.discordapp.com/attachments/717853456244670509/720344286650040370/PogChamp.png")
    await ctx.send(embed=pog_card)

@client.command
async def f(ctx):
    f_card = discord.Embed(colour = discord.Colour.green())
    f_card.set_image(url="https://cdn.discordapp.com/attachments/717853456244670509/720345633734787512/pressf.jpg")
    await ctx.send(embed=f_card)

@client.command()
async def meme(ctx):
    memes=["https://bit.ly/3cSmj3Y", "https://bit.ly/3fcPaSs", "https://bit.ly/3cStvNy", "https://bit.ly/3ffmWXd", "https://bit.ly/2YkpGM5",
     "https://bit.ly/2YnYn3f", "https://bit.ly/2zpc8q8", "https://bit.ly/3fcwPVv", "https://bit.ly/3hbCOMd", "https://bit.ly/3f5FWam"]
    meme_card = discord.Embed(colour = discord.Colour.green())
    meme_card.set_image(url=random.choice(memes))
    await ctx.send(embed=meme_card)

@client.command()
async def vote(ctx):
    vote_card = discord.Embed(title="\U0001F3C6 Vote for Synergyy on Top.gg", description="Thanks for helping us grow!", colour = discord.Colour.green())
    vote_card.add_field(name="Vote", value="[Click here to vote!](https://www.youtube.com)")
    vote_card.set_footer(text="Tip: You can vote for us once every 12 hours.\nTip: Votes are worth double on weekends.")
    await ctx.send(embed=vote_card)

@client.command(pass_context=True) #Custom Help Command
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.green(),)
    embed.set_author(name='Help', icon_url="https://cdn.discordapp.com/attachments/717853456244670509/718935942605439006/Screen_Shot_2020-06-06_at_5.14.29_PM.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/717853456244670509/718950987762761758/SynergyyNoBg.png")
    embed.add_field(name='!meeting', value = 'Creates a new meeting.\n>>> eg. !meeting "Physics Project" in 2 hours\neg. !meeting "Math Meeting!" on 8/21 at 9:30 PM\neg. !meeting "Team Discussion" on June 19 at 3pm', inline=False)
    embed.add_field(name='!poll', value = 'Creates a new poll.\n>>> Format: !poll "Title" options (poll time limit in minutes)\neg. !poll "Favourite Food?" Pizza, Sushi, Tacos 2\nNote: The poll must have atleast 2 options.', inline=False)
    embed.add_field(name='!clear (# of messages)', value = 'Clears messages from the current channel.\n>>> eg. !clear 10\nNote: If no number is provided, 10 is the default value.', inline=False)
    embed.add_field(name='!8ball', value = 'Asks the magical 8ball for an answer to your question.\n>>> eg. !8ball Will I become succesful?', inline=False)
    embed.add_field(name='!ping', value = 'Returns the bot\'s latency.', inline=False)
    embed.add_field(name='!flip', value = 'Flips a coin!', inline=False)
    embed.add_field(name='!vote', value = 'Vote for us on Top.gg to help us grow!', inline=False)
    #embed.add_field(name='-------------------------------------', value = "Visit our [website](https://www.youtube.com/) for more help!", inline=False)
    embed.set_footer(text="Tip: All commands can be invoked using !")

    await ctx.send(embed=embed)

@client.command() #Meeting Creation Command + Reminder
async def meeting(ctx, *, information):
    info = information.strip().split()
    name = time = date = ''
    time_missing = discord.Embed(title='Missing Meeting Time!', description="For further help, please refer to !help", colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description='Please put the name in quotations:\neg. !meeting "Physics Project" in 2 hours\nFor more info, please refer to !help', colour=discord.Color.green())

    for i in range(len(info)):
        for j in range(len(timescales)):
            #If user requests a meeting IN a certain amount of time
            if timescales[j] in info[i].lower() and i >= 1:

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

                #Create embeds and Send
                meeting_card = discord.Embed(title=f"\U0001F5D3 Meeting Created: {name}", colour=discord.Colour.green())
                meeting_card.add_field(name="Meeting Time", value=f"{time} on {date}")
                meeting_card.set_footer(text=f"Tip: I will remind you about this meeting when its starting!")

                await ctx.send(content=None, embed=meeting_card) 
                await asyncio.sleep(m_time-now)

                reminder_card = discord.Embed(colour = discord.Colour.green())
                reminder_card.set_author(name="Hey! This is a reminder about your meeting, \"{0}\".\nHead over to your team's discord server to participate!".format(name))
                await ctx.author.send(content=None, embed=reminder_card)

                announce = discord.Embed(colour=discord.Colour.green())
                announce.set_author(name=f"\U00002755 Attention! The meeting \"{name}\" is starting now.")
                await ctx.send(embed=announce)
                return        
    
    if '"' in information:
        name = information[information.index('"')+1 : information.rindex('"')]
        if has_date(information[information.rindex('"')+1:]):
            d = parse(information[information.rindex('"')+1:])
            now = datetime.datetime.now().timestamp()
            m_time = d.timestamp()
            time = d.strftime('%-I:%M%p')
            date = d.strftime('%A, %b %-d, %Y')

            meeting_card = discord.Embed(title=f"\U0001F5D3 Meeting Created: {name}", colour=discord.Colour.green())
            meeting_card.add_field(name="Meeting Time", value=f"{time} on {date}")
            meeting_card.set_footer(text=f"Tip: I will remind you about this meeting when its starting!")

            await ctx.send(content=None, embed=meeting_card)
            await asyncio.sleep(m_time-now)

            reminder_card = discord.Embed(colour = discord.Colour.green())
            reminder_card.set_author(name="Hey! This is a reminder about your meeting, \"{0}\".\nHead over to your team's discord server to participate!".format(name))
            
            await ctx.author.send(content=None, embed=reminder_card)

            announce = discord.Embed(colour=discord.Colour.green())
            announce.set_author(name=f"\U00002755 Attention! The meeting \"{name}\" is starting now.")
            await ctx.send(embed=announce)

        else:
            await ctx.send(content=None, embed=time_missing)
    else:
        await ctx.send(content=None, embed=format_error)

@client.command()
async def poll(ctx, *, information):
    if '\"' in information and ',' in information and information[len(information)-1].isnumeric():
        op = []
        polltimeinminutes = 0
        title = information[information.index('\"')+1 : information.rindex('\"')]
        temp = information.rindex('\"')
        for i in range(information.rindex('\"')+1, len(information)):
            if information[i] == ',':
                op.append(information[temp+1:i].strip())
                temp = i
        for j in reversed(information):
            if not j.isnumeric():
                polltimeinminutes = int(information[information.rindex(j)+1:].strip())
                break
        op.append(information[temp+1 : information.rindex(str(polltimeinminutes))].strip())

        if len(op) <= 20:

            options = {}
            for i in range(len(op)):
                options[unicode_block[i]] = op[i]
            
            vote = discord.Embed(title=f"\U0001F4F6 {title}", color=discord.Colour.green()) 
            value = "\n".join("{} - {}".format(*item) for item in options.items())
            vote.add_field(name="Options:", value=value, inline=False) 
            vote.set_footer(text="Time to vote: %s minute.\nUse the reactions below to vote." % (polltimeinminutes))

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
        
        else:
            too_many_options = discord.Embed(title="Too many options!", description="The limit for !poll is 20 options.", color=discord.Colour.green())
            await ctx.send(embed=too_many_options)

#Command Specific Error Handling--------------------------

@clear.error
async def clear_error(ctx, error):
    arg_missing = discord.Embed(title='Missing Required Argument!', description="You must specify a number of messages to clear!\neg. !clear 50\n Please refer to !help for more info.", colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=arg_missing)

@_8ball.error
async def _8ball_error(ctx, error):
    arg_missing = discord.Embed(title='Missing Required Argument!', description="You need to ask the 8ball a question!\neg. !8ball Am I cool?\n Please refer to !help for more info.", colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description="Please follow this format: !8ball Am I cool?\n Please refer to !help for more info.", colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=arg_missing)
    else:
        await ctx.send(content=None, embed=format_error)

@meeting.error
async def meeting_error(ctx, error):
    time_missing = discord.Embed(title='Missing Meeting Time!', description="For further help, please refer to !help", colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description='Please put the name in quotations:\neg. !meeting "Physics Project" in 2 hours', colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=time_missing)
    else:
        await ctx.send(content=None, embed=format_error)

@poll.error
async def poll_error(ctx, error):
    arg_missing = discord.Embed(title='Missing Required Argument!', description="Please follow this format: !poll \"Title\" option1, option2, option3 1\n Please refer to !help for more info.", colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description="Please follow this format: !poll \"Title\" option1, option2, option3 1\n Please refer to !help for more info.", colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=arg_missing)
    else:
        await ctx.send(content=None, embed=format_error)

#Other Functions------------------------------------------

def has_date(string, fuzzy=True):
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

#Bot Token Pairing--------------------------------
client.run('TOKEN')
