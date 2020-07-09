import discord
import os
from discord.ext import commands, tasks, timers
import random
import datetime
import time
import asyncio
from word2number import w2n
from dateutil.parser import parse
import sqlite3
from operator import itemgetter
from pytz import timezone

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

@client.command(pass_context=True) #Custom Help Command
async def help(ctx):
    embed = discord.Embed(title="\U00002754	Help", colour = discord.Colour.green())
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/717853456244670509/718950987762761758/SynergyyNoBg.png")
    embed.add_field(name='!meeting', value = 'Creates a new meeting.\nOnce the meeting is created, you can easily add it to your google calendar.\n>>> eg. !meeting "Physics Project" in 2 hours\neg. !meeting "Math Meeting!" on 8/21 at 9:30 PM\neg. !meeting "Team Discussion" on June 19 at 3pm', inline=False)
    embed.add_field(name='!list', value = 'Lists all upcoming meetings.', inline=False)
    embed.add_field(name='!delete', value = 'Delete upcoming meetings.', inline=False)
    embed.add_field(name='!addtodo', value = 'Creates a new task.\n>>> eg. !addtodo Finish Powerpoint', inline=False)
    embed.add_field(name='!todo', value = 'Allows you to view and complete items in your todo list.', inline=False)
    embed.add_field(name='!poll', value = 'Creates a new poll.\n>>> Format: !poll "Title" options (poll time limit in minutes)\neg. !poll "Favourite Food?" Pizza, Sushi, Tacos 2\nNote: The poll must have atleast 2 options.', inline=False)
    embed.add_field(name='-------------------------------------', value = "Visit our [website](https://www.synergyy.ml/) for the full list of commands!\nVote for us on [top.gg](https://top.gg/bot/719271108037312595) to help us grow!", inline=False)
    embed.set_footer(text="Tip: All commands can be invoked using !")
    await ctx.send(embed=embed)

@client.command() #Ping Command
async def ping(ctx):
    await ctx.send(f'Pong! My current latency is {round(client.latency*1000)}ms.')

@client.command(pass_context=True) #Clear Messages Command
@commands.has_permissions(manage_messages=True)
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
    vote_card.add_field(name="Vote", value="[Click here to vote for free!](https://top.gg/bot/719271108037312595)")
    vote_card.set_footer(text="Tip: You can vote once every 12 hours.\nTip: Votes are worth double on weekends.")
    await ctx.send(embed=vote_card)

@client.command()
async def addtodo(ctx, *, todo_item):
    todo_add_card = discord.Embed(title="\U0001F4CB To-Do Item Added!", colour=discord.Color.green())
    todo_add_card.add_field(name="Item Added:", value=f">>> **{todo_item}** was added to your todo list.")
    todo_add_card.set_footer(text="Use !todo to see your list and to check off items when you complete them.")
    await ctx.send(embed=todo_add_card)

    #Storing Todo Data
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    sql = ("INSERT INTO todo VALUES(?,?,?)")
    val = (ctx.guild.id, ctx.channel.id, todo_item)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

@client.command()
async def todo(ctx):
    todo_card = discord.Embed(title="\U0001F4CB Todo List", colour=discord.Colour.green())
    completed_embed = discord.Embed(title='Todo Item Completed!', colour=discord.Colour.green())

    #Accessing data
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT todo_item FROM todo WHERE guild_id = {ctx.guild.id}")
    todos = [[todo[0]] for todo in cursor.fetchall()]

    for i in range(len(todos)):
        todos[i].insert(0, unicode_block[i])

    #Displaying todo items
    values = []
    for todo in todos:
        values.append(f"{todo[0]} - **{str(todo[1])}**")
    if values:
        todo_card.add_field(name="Tasks", value='>>> ' + '\n'.join(values), inline=False)
        todo_card.set_footer(text="Select the corresponding emojis and press the ✅ to complete your items.")

        #Get complete choices
        message1 = await ctx.send(embed=todo_card)
        for todo in todos:
            await message1.add_reaction(emoji=todo[0])
        await message1.add_reaction(emoji='✅')

        tb_deleted = []
        while True:
            message1 = await ctx.fetch_message(message1.id)
            counts = {react.emoji: react.count for react in message1.reactions}
            if counts['✅'] > 1:
                for count in counts:
                    if counts[count] > 1:
                        tb_deleted.append(count)
                break
        
        #Delete choices
        dtodos = []
        for todo in todos:
            for dl in tb_deleted:
                if todo[0] == dl:
                    sql = 'DELETE FROM todo WHERE todo_item=? AND guild_id=?'
                    val = (todo[1], ctx.guild.id)
                    cursor.execute(sql, val)
                    dtodos.append(todo[1])
        deleted_todos = "\n".join(f"**{d}** successfully completed!" for d in dtodos)
        if not dtodos:
            todo_opt_missing = discord.Embed(title='No Todo Item Selected!', description="Please try again and select a todo item to complete using the reactions.", colour=discord.Color.green())
            await ctx.send(embed=todo_opt_missing)
        else:
            completed_embed.add_field(name='Items Completed:', value='>>> ' + deleted_todos, inline=False)
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(embed=completed_embed)
    else:
        todo_card.description = "No current todo items at this time."
        await ctx.send(embed=todo_card)

@client.command() #Meeting Creation Command + Reminder
async def meeting(ctx, *, information):
    info = information.strip().split()
    name = time = date = ''
    time_missing = discord.Embed(title='Missing Meeting Time!', description="For further help, please refer to !help", colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description='Please put the name in quotations:\neg. !meeting "Physics Project" in 2 hours\nFor more info, please refer to !help', colour=discord.Color.green())
    on_condition = True

    for i in range(len(info)):
        for j in range(len(timescales)):
            #If user requests a meeting IN a certain amount of time
            if timescales[j] in info[i].lower() and i >= 1:
                on_condition = False

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
                
                name = str(name).strip('\"')
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

    if on_condition:
        if '"' in information:
            name = information[information.index('"')+1 : information.rindex('"')]
            if has_date(information[information.rindex('"')+1:]):
                d = parse(information[information.rindex('"')+1:])
                now = datetime.datetime.now().timestamp()
                m_time = d.timestamp()
                time = d.strftime('%-I:%M%p')
                date = d.strftime('%A, %b %-d, %Y')
            else:
                await ctx.send(content=None, embed=time_missing)
        else:
            await ctx.send(content=None, embed=format_error)

    #Data Storage
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    sql = ("INSERT INTO meetings VALUES(?,?,?,?,?)")
    val = (ctx.guild.id, ctx.channel.id, name, m_time, None)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

    #Create Google Calendar Link
    google_date = datetime.datetime.fromtimestamp(m_time).strftime('%Y%m%d')
    google_time = datetime.datetime.fromtimestamp(m_time).strftime('%H%M%S')
    google_end_date = datetime.datetime.fromtimestamp(m_time + 3600).strftime('%Y%m%d')
    google_end_time = datetime.datetime.fromtimestamp(m_time + 3600).strftime('%H%M%S')
    google_name = '+'.join(name.split())
    google_link = 'https://www.google.com/calendar/render?action=TEMPLATE&text='+google_name+'&details=Event+created+by+Synergyy&dates='+google_date+'T'+google_time+'/'+google_end_date+'T'+google_end_time
    print(google_link)

    #Meeting Confirmation
    meeting_card = discord.Embed(title=f"\U0001F5D3 Meeting Created: {name}", url=google_link, colour=discord.Colour.green())
    meeting_card.add_field(name="Meeting Time", value=f"{time} on {date}")
    meeting_card.set_footer(text="Tip: I will remind you about this meeting when its starting!\nTip: Click the title to add this event to Google Calendar!")
    confirmation = await ctx.send(content=None, embed=meeting_card)
    await confirmation.add_reaction(emoji='✅')
    await asyncio.sleep(m_time-now)

    #Check if event still exists
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    sql= "SELECT rowid FROM meetings WHERE meeting_name=? AND guild_id=? AND meeting_time=?"
    val = (name, ctx.guild.id, m_time)
    cursor.execute(sql, val)
    data = cursor.fetchone()
    
    if data:
    #Meeting DM Reminder
        rvsp = []
        message = await ctx.channel.fetch_message(confirmation.id)
        for reaction in message.reactions:
            if str(reaction) == '✅':
                rvsp = await reaction.users().flatten()
            rvsp = rvsp[1:]

        url = "http://discordapp.com/channels/" + str(confirmation.guild.id) + '/' + str(confirmation.channel.id) + '/' + str(confirmation.id)
        reminder_card = discord.Embed(description=f"Hey! This is a reminder about your meeting, [{name}]({url}).\nHead over to your team's discord server to participate!", colour = discord.Colour.green())
        for member in rvsp:
            dm = await member.create_dm()
            await dm.send(embed=reminder_card)

        #Meeting Server Announce
        announce = discord.Embed(colour=discord.Colour.green())
        announce.set_author(name=f"\U00002755 Attention! The meeting \"{name}\" is starting now.")
        await ctx.send(embed=announce)

        #Delete meeting for database
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        sql = 'DELETE FROM meetings WHERE meeting_name=? AND guild_id=?'
        val = (name, ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

@client.command()
async def poll(ctx, *, information): #Poll command
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

@client.command()
async def list(ctx): #List command that lists all upcoming meetings
    meetings_embed = discord.Embed(title="\U0001F4CB Upcoming Meetings", colour=discord.Colour.green())

    #Accessing data
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT meeting_name FROM meetings WHERE guild_id = {ctx.guild.id}")
    meetings = [[meeting[0]] for meeting in cursor.fetchall()]
    cursor.execute(f"SELECT meeting_time FROM meetings WHERE guild_id = {ctx.guild.id}")
    i = 0
    for meeting_time in cursor.fetchall():
        meetings[i].append(meeting_time[0])
        i += 1
    meetings.sort(key=itemgetter(1))
    
    #Converting data
    if meetings:
        today = []
        week = []
        future = []
        for i in range(len(meetings)):
            date = datetime.datetime.fromtimestamp(int(meetings[i][1])).strftime('%A, %b %-d, %Y')
            time = datetime.datetime.fromtimestamp(int(meetings[i][1])).strftime('%-I:%M%p')
            if datetime.datetime.fromtimestamp(int(meetings[i][1])).date() <= datetime.datetime.today().date():
                today.append(f"**{str(meetings[i][0])}** on {date} at {time}")
            elif datetime.datetime.fromtimestamp(int(meetings[i][1])).date() <= datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()+604800).date():
                week.append(f"**{str(meetings[i][0])}** on {date} at {time}")
            else:
                future.append(f"**{str(meetings[i][0])}** on {date} at {time}")
        if today:
            meetings_embed.add_field(name="Today", value='>>> ' + '\n'.join(today), inline=False)
        if week:
            meetings_embed.add_field(name="This Week", value='>>> ' + '\n'.join(week), inline=False)
        if future:
            meetings_embed.add_field(name="Later", value='>>> ' + '\n'.join(future), inline=False)
    else:
        meetings_embed.add_field(name="No upcoming meetings.", value=">>> Use !meeting to create one!\nRefer to !help for more info.")

    await ctx.send(embed=meetings_embed)

@client.command()
async def delete(ctx, *, name=None):
    deleted_embed = discord.Embed(title='Delete Meeting', colour=discord.Colour.green())
    if name:
        gt_10 = False

        #Accessing data
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        sql = "SELECT meeting_name FROM meetings WHERE meeting_name=? AND guild_id=?"
        val = (name, ctx.guild.id)
        cursor.execute(sql, val)
        meetings = [[meeting[0]] for meeting in cursor.fetchall()]

        #If there is only one meeting with entered name
        if len(meetings) == 1:
            sql = 'DELETE FROM meetings WHERE meeting_name=? AND guild_id=?'
            val = (name, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            deleted_embed.add_field(name='Meeting Deleted:', value=f'>>> {name} successfully deleted')
            await ctx.send(embed=deleted_embed)
            return

        #If there is more than one meeting with entered name and exceeds 10
        elif len(meetings) > 10:
            meetings = meetings[:10]
            gt_10 = True

        elif len(meetings) == 0:
            no_option = discord.Embed(title='Meeting Not Found', description='>>> No meetings found with that name.', colour=discord.Colour.green())
            await ctx.send(embed=no_option)
            return

        #Getting Meeting time to display
        sql = "SELECT meeting_time FROM meetings WHERE meeting_name=? AND guild_id=?"
        val = (name, ctx.guild.id)
        cursor.execute(sql, val)
        i = 0
        for meeting_time in cursor.fetchall():
            meetings[i].append(meeting_time[0])
            meetings[i].insert(0, unicode_block[i])
            i += 1
            if i >= len(meetings):
                break
        meetings.sort(key=itemgetter(2))

        #Displaying options
        values = []
        for i in range(len(meetings)):
            date = datetime.datetime.fromtimestamp(int(meetings[i][2])).strftime('%b %-d, %Y')
            time = datetime.datetime.fromtimestamp(int(meetings[i][2])).strftime('%-I:%M%p')
            values.append(f"{meetings[i][0]} - **{str(meetings[i][1])}** on {date} at {time}")
        delete_options = discord.Embed(title='Delete Meeting', colour=discord.Colour.green())
        delete_options.add_field(name="Select meetings to delete", value='>>> ' + '\n'.join(values), inline=False)
        delete_options.set_footer(text="Use the reactions below to select which meetings to delete, then click the checkmark to confirm.")

        #If original meetings list was greater than 10
        if gt_10:
            delete_options.add_field(name='\u200b', value='Results exceed display limit. Try using !delete *meeting name* to narrow your search', inline=False)

        #Adding reactions to get choices
        message_1 = await ctx.send(embed=delete_options)
        for meeting in meetings:
            await message_1.add_reaction(emoji=meeting[0])
        await message_1.add_reaction(emoji='✅')

        #getting choices
        tb_deleted = []
        while True:
            message_1 = await ctx.fetch_message(message_1.id)
            counts = {react.emoji: react.count for react in message_1.reactions}
            if counts['✅'] > 1:
                for count in counts:
                    if counts[count] > 1:
                        tb_deleted.append(count)
                break

        #Delete choices
        dmeetings = []
        for meeting in meetings:
            for dl in tb_deleted:
                if meeting[0] == dl:
                    sql = 'DELETE FROM meetings WHERE meeting_name=? AND guild_id=? AND meeting_time=?'
                    val = (meeting[1], ctx.guild.id, meeting[2])
                    cursor.execute(sql, val)
                    dmeetings.append(meeting[1])
        deleted_meetings = "\n".join(f"**{d}** successfully deleted" for d in dmeetings)

        if not dmeetings:
            meeting_opt_missing = discord.Embed(title="No Meeting Selected!", description="Please try again and select a meetnig to delete using the reactions.")
            await ctx.send(embed=meeting_opt_missing)
        else:
            deleted_embed.add_field(name='\u200b', value='>>> ' + deleted_meetings, inline=False)

            db.commit()
            cursor.close()
            db.close()
            await ctx.send(embed=deleted_embed)
        
    else:
        gt_10 = False

        #Accessing data
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT meeting_name FROM meetings WHERE guild_id = {ctx.guild.id}")
        meetings = [[meeting[0]] for meeting in cursor.fetchall()]

        if len(meetings) > 10:
            meetings = meetings[:10]
            gt_10 = True
        elif len(meetings) == 0:
            no_option = discord.Embed(title='Meeting Not Found', description='>>> No meetings found.', colour=discord.Colour.green())
            await ctx.send(embed=no_option)
            return

        #Getting Meeting time to display
        cursor.execute(f"SELECT meeting_time FROM meetings WHERE guild_id = {ctx.guild.id}")
        i = 0
        for meeting_time in cursor.fetchall():
            meetings[i].append(meeting_time[0])
            meetings[i].insert(0, unicode_block[i])
            i += 1
            if i >= len(meetings):
                break
        meetings.sort(key=itemgetter(2))

        #Displaying options
        values = []
        for i in range(len(meetings)):
            date = datetime.datetime.fromtimestamp(int(meetings[i][2])).strftime('%b %-d, %Y')
            time = datetime.datetime.fromtimestamp(int(meetings[i][2])).strftime('%-I:%M%p')
            values.append(f"{meetings[i][0]} - **{str(meetings[i][1])}** on {date} at {time}")
        delete_options = discord.Embed(title='Delete Meeting', colour=discord.Colour.green())
        delete_options.add_field(name="Select meetings to delete", value='>>> ' + '\n'.join(values), inline=False)
        
        #If original meetings list was greater than 10
        if gt_10:
            delete_options.add_field(name='\u200b', value='Results exceed display limit. Try using !delete *meeting name* to narrow your search', inline=False)

        #Adding reactions to get choices
        message_1 = await ctx.send(embed=delete_options)
        for meeting in meetings:
            await message_1.add_reaction(emoji=meeting[0])
        await message_1.add_reaction(emoji='✅')

        #getting choices
        tb_deleted = []
        while True:
            message_1 = await ctx.fetch_message(message_1.id)
            counts = {react.emoji: react.count for react in message_1.reactions}
            if counts['✅'] > 1:
                for count in counts:
                    if counts[count] > 1:
                        tb_deleted.append(count)
                break

        #Delete choices
        dmeetings = []
        for meeting in meetings:
            for dl in tb_deleted:
                if meeting[0] == dl:
                    sql = 'DELETE FROM meetings WHERE meeting_name=? AND guild_id=? AND meeting_time=?'
                    val = (meeting[1], ctx.guild.id, meeting[2])
                    cursor.execute(sql, val)
                    dmeetings.append(meeting[1])
        deleted_meetings = "\n".join(f"**{d}** successfully deleted" for d in dmeetings)
        deleted_embed.add_field(name='\u200b', value='>>> ' + deleted_meetings, inline=False)

        db.commit()
        cursor.close()
        db.close()
        await ctx.send(embed=deleted_embed)

@client.command()
async def timenow(ctx):
    fmt = "**%H:%M** on %Y-%m-%d "
    #Timezone Conversions
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_london = now_utc.astimezone(timezone('Europe/London'))
    now_berlin = now_utc.astimezone(timezone('Europe/Berlin'))
    #now_cet = now_utc.astimezone(timezone('CET'))
    now_israel = now_utc.astimezone(timezone('Israel'))
    now_dubai = now_utc.astimezone(timezone("Asia/Dubai"))
    now_pakistan = now_utc.astimezone(timezone('Asia/Karachi'))
    now_india = now_utc.astimezone(timezone('Asia/Kolkata'))
    now_bangladesh = now_utc.astimezone(timezone('Asia/Dhaka'))
    now_phnom = now_utc.astimezone(timezone('Asia/Phnom_Penh'))
    now_china = now_utc.astimezone(timezone('Asia/Hong_Kong'))    
    now_japan = now_utc.astimezone(timezone('Asia/Tokyo')) 
    now_australia = now_utc.astimezone(timezone('Australia/Sydney')) 
    now_edmonton = now_utc.astimezone(timezone('America/Edmonton'))   
    now_canada_east = now_utc.astimezone(timezone('Canada/Eastern'))
    now_central = now_utc.astimezone(timezone('US/Central'))
    #now_pacific = now_utc.astimezone(timezone('US/Pacific'))

    currenttime_card = discord.Embed(title="\U0001F551 Current International Times", colour = discord.Colour.green())

    currenttime_card.add_field(name="Coordinated Universal Time (UTC+0)", value=f">>> {now_utc.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="London (UTC+1/BST)", value=f">>> {now_london.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="\u200b", value=f"\u200b", inline=True)

    currenttime_card.add_field(name="Berlin (UTC+2/CET)", value=f">>> {now_berlin.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="Israel and East Africa (UTC+3/IDT)", value=f">>> {now_israel.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="\u200b", value=f"\u200b", inline=True)

    currenttime_card.add_field(name="Dubai (UTC+4/GST)", value=f">>> {now_dubai.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="Pakistan (UTC+5/PLT)", value=f">>> {now_pakistan.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="\u200b", value=f"\u200b", inline=True)

    currenttime_card.add_field(name="India (UTC+5.5/IST)", value=f">>> {now_india.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="Bangladesh (UTC+6/BST)", value=f">>> {now_bangladesh.strftime(fmt)}", inline=True) 
    currenttime_card.add_field(name="\u200b", value=f"\u200b", inline=True)

    currenttime_card.add_field(name="Thailand and Vietnam (UTC+7/ICT)", value=f">>> {now_phnom.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="China (UTC+8/CST)", value=f">>> {now_china.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="\u200b", value=f"\u200b", inline=True)

    currenttime_card.add_field(name="Japan (UTC+9/JST)", value=f">>> {now_japan.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="Sydney (UTC+10/AEST)", value=f">>> {now_australia.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="\u200b", value=f"\u200b", inline=True)

    currenttime_card.add_field(name="Canada Eastern (UTC-4/EDT)", value=f">>> {now_canada_east.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="US Central (UTC-5/CDT)", value=f">>> {now_central.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="\u200b", value=f"\u200b", inline=True)

    currenttime_card.add_field(name="Central Standard (UTC-6/CST)", value=f">>> {now_edmonton.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="US Pacific (UTC-7/PDT)", value=f">>> {now_central.strftime(fmt)}", inline=True)
    currenttime_card.add_field(name="\u200b", value=f"\u200b", inline=True)

    currenttime_card.set_footer(text="Tip: UTC and GMT are interchangable.")
    await ctx.send(embed=currenttime_card)

#Command Specific Error Handling--------------------------

@clear.error
async def clear_error(ctx, error):
    arg_missing = discord.Embed(title='Missing Required Argument!', description="You must specify a number of messages to clear!\neg. !clear 50\n Please refer to !help for more info.", colour=discord.Color.green())
    perms_missing = discord.Embed(title="Missing Permissions!", description="You must have the Manage Messages Permission to run this command.", colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=arg_missing)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(content=None, embed=perms_missing)
    else:
        print(error)

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
        print(error)

@poll.error
async def poll_error(ctx, error):
    arg_missing = discord.Embed(title='Missing Required Argument!', description="Please follow this format: !poll \"Title\" option1, option2, option3 1\n Please refer to !help for more info.", colour=discord.Color.green())
    format_error = discord.Embed(title='Format Error!', description="Please follow this format: !poll \"Title\" option1, option2, option3 1\n Please refer to !help for more info.", colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=arg_missing)
    else:
        await ctx.send(content=None, embed=format_error)

@list.error
async def list_error(ctx, error):
    print(error)

@delete.error
async def delete_error(ctx, error):
    print(error)

@addtodo.error
async def addtodo_error(ctx, error):
    item_missing = discord.Embed(title='Missing Todo Item!', description="For further help, please refer to !help", colour=discord.Color.green())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=item_missing)
    else:
        print(error)

@todo.error
async def todo_error(ctx, error):
    print(error)

#Other Functions------------------------------------------

def read_token():
    with open("token.txt", 'r') as f:
        lines = f.readlines()
        return lines[0].strip()

def has_date(string, fuzzy=True):
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

#Bot Token Pairing--------------------------------
client.run(read_token())