import requests
import discord
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands,tasks
import pafy
import ffmpeg
import subprocess
import os
import time
import shlex

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

# Custom
import NiMan_Constants as constants
import NiMan_Helper as helper
import NiMan_START as main

global bot
bot = main.bot

def setup(bot):
    print('Setting up commands')

# Commands
@bot.command(name='test', help='test')
async def test(ctx):
    print('test command')
    await ctx.send('Test command success.')

@bot.command(name='dj', help='displays the status of the local minecraft server')
async def dj(ctx):
    print('getting status of dj server')
    #output = subprocess.check_output("mcstatus 127.0.0.1 status", shell=True)
    #os.system('mcstatus 127.0.0.1 status')

    proc = subprocess.Popen(["mcstatus", "127.0.0.1", "status"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    s = out.decode('utf-8')
    if 'players' not in s:
        print("Server request timed out")
        await ctx.send("Server request timed out, server not running or still starting")
        return
    players = s[s.find('players'):]
    print(players)
    await ctx.send(players[9:])

    args = shlex.split('tasklist /FI \"imagename eq java.exe\" | findstr \" K$\"')
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    s = out.decode('utf-8')
    print(s)
    await ctx.send(s)

@bot.command(name='djrestart', help='Kills java.exe and restarts the server. CAREFUL, this could result in data loss as it TASKKILLs the server process.')
async def djrestart(ctx):
    print('killing java.exe')
    await ctx.send('killing server (java.exe)')
    command = 'taskkill /IM "java.exe" /F'
    os.system(command)
    time.sleep(2)
    print('starting server')
    await ctx.send('starting server (run.bat)')
    run = 'C:\\Users\\Admin\\Downloads\\mcss_win-x86-64_v11.13.0\\servers\\DivineJourney2\\run.lnk'
    os.startfile(run)
    await ctx.send('please wait 10 min for server to start')

@bot.command(name='djlog', help='displays the latest.log file from the minecraft server')
async def djlog(ctx):
    with open('C:\\Users\\Admin\\Downloads\\mcss_win-x86-64_v11.13.0\\servers\\DivineJourney2\\logs\\latest.log') as latestLog:
        lines = latestLog.readlines()
        lastLines = lines[max(-50, (-len(lines) + 1)):]
        with open('latest.log', 'w') as outputLog:
            for line in lastLines:
                outputLog.write(line)
            outputLog.close()
    await ctx.send(file=discord.File('latest.log', 'latest.log'))

@bot.command(name='play')
async def play(ctx):

    search = ctx.message.content[5:]

    user = ctx.message.author
    if len(ctx.message.mentions) != 0:
        user = ctx.message.mentions[0]

    if user.voice == None:
        await ctx.send(user.name + ' is not in a voice channel.')
        return

    channel = user.voice.channel
    #channel.connect()
    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)

    voice_client = await voice.connect()

    search = search.replace(" ", "+")

    response = requests.get("https://www.youtube.com/results?search_query=" + search)
    start = response.text.find('\"videoId\":\"') + 11
    end = response.text.find('\",', start + 1)
    videoId = response.text[start:end]
    print(videoId)

    await ctx.send("https://www.youtube.com/watch?v=" + videoId)

    song = pafy.new(videoId)  # creates a new pafy object

    audio = song.getbestaudio()  # gets an audio source

    source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use

    voice_client.play(source)  # play the source

@bot.command(name='presence', help='Changes the presence of the bot.')
async def presence(ctx):
    message = ctx.message.content
    try:
        type = message.split(' ')[1]
    except:
        type = 'p'

    # Playing
    if type == 'p' or type == 'play' or type == 'playing':
        try:
            name = message.split('\"')[1]
        except:
            name = ''
        await bot.change_presence(activity=discord.Game(name=name))
    # Streaming
    elif type == 's' or type == 'stream' or type == 'streaming':
        try:
            name = message.split('\"')[1]
        except:
            name = ''
        try:
            url = message.split('\"')[3]
        except:
            url = ''
        await bot.change_presence(activity=discord.Streaming(name=name,url=url))
    # Watching
    elif type == 'w' or type == 'watch' or type == 'watching':
        try:
            name = message.split('\"')[1]
        except:
            name = ''
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name))
    # Listening
    elif type == 'l' or type == 'listen' or type == 'listening':
        try:
            name = message.split('\"')[1]
        except:
            name = ''
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=name))

@bot.command(name='getuserid', help='Gets user IDs')
async def getuserid(ctx):
    if '[test]' in ctx.message.content:
        username = ctx.message.author.name
        print(username)
        print('-> ' + str(helper.get_id(ctx.message.guild.members, username)))
        return
    users = []
    for user in ctx.message.mentions:
        users.append(user)
    for channel in ctx.message.channel_mentions:
        for user in channel.members:
            users.append(user)
    if len(users) == 0:
        users.append(ctx.message.author)
    print(ctx.message.author.name + ' requested user ids.')
    for user in users:
        print(user.name + ' -> ' + str(user.id))
        await ctx.send(user.name + ' -> ' + str(user.id))

@bot.command(name='getchanid', help='Gets channel IDs')
async def getchanid(ctx):
    channels = []
    for channel in ctx.message.channel_mentions:
        channels.append(channel)
    if len(channels) == 0:
        channels.append(ctx.message.channel)
    print(ctx.message.author.name + ' requested channel ids')
    for channel in channels:
        print(channel.name + ' -> ' + str(channel.id))
        await ctx.send(channel.name + ' -> ' + str(channel.id))

@bot.command(name='getguildid', help='Gets guild ID')
async def getguildid(ctx):
    print(ctx.message.author.name + ' requested the guild id')
    print(ctx.message.guild.name + ' -> ' + str(ctx.message.guild.id))
    await ctx.send(ctx.message.guild.name + ' -> ' + str(ctx.message.guild.id))

@bot.command(name='purge', help='[prefix]purge [channel] [user] [#], defaults to current channel and user, but more than one channel and/or user may be specified.')
async def purge(ctx):
    await ctx.message.delete()
    if ctx.message.author.name not in constants.admin_list:
        await ctx.send('Sorry <@' + str(ctx.message.author.id) + '>, you do not have permission to use that command. Please see <@' + constants.user_Striker1521_0430 + '>')
        print(ctx.message.author.name + ' tried to purge messages but it failed.')
        return
    message = str.strip(ctx.message.content)
    try:
        limit = int(message.split(' ')[len(message.split(' ')) - 1])
        if not str.isnumeric(limit) or limit <= 0:
            limit = 100
    except:
        print('ignoring exception')
        limit = 100
    channels = ctx.message.channel_mentions
    if len(channels) == 0:
        channels = []
        channels.append(ctx.message.channel)
    users = ctx.message.mentions
    if len(users) == 0:
        users = []
        users.append(bot.user)
    for channel in channels:
        for user in users:
            helper.focused_user = user
            deleted = await channel.purge(limit=limit,check=helper.is_user,bulk=True)
            print(ctx.message.author.name + ' deleted {} of '.format(len(deleted)) + user.name + '\'s messages in ' + channel.name)
            await ctx.send('<@' + str(ctx.message.author.id) + '>' + ' deleted {} of '.format(len(deleted)) + '<@' + str(user.id) + '>' + '\'s message(s)' + ' in ' + '<#' + str(channel.id) + '>')

# Voice Channel Stuff
@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    user = ctx.message.author
    if len(ctx.message.mentions) != 0:
        user = ctx.message.mentions[0]
    print('joining voice')
    if not user.voice:
        await ctx.send(user.name + ' is not connected to a voice channel')
    else:
        channel = user.voice.channel
        await channel.connect()

@bot.command(name='leave', help='Tells the bot to leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client != None and voice_client.is_connected():
        print('leaving voice')
        await voice_client.disconnect()
    else:
        await ctx.send('I am not connected to a voice channel.')



@bot.command(name='quote', help='Gets an inpirational quote')
async def quote(ctx):
    await ctx.send(helper.get_inspirational_quote())

@bot.command(name='rsquote', help='Gets a Ron Swanson quote')
async def rsquote(ctx):
    await ctx.send(helper.get_rs_quote())

@bot.command(name='cnquote', help='Gets a Chuck Norris quote')
async def cnquote(ctx):
    await ctx.send(helper.get_cn_quote())

@bot.command(name='joke', help='Gets a joke')
async def joke(ctx):
    type = ''
    if len(ctx.message.content) > 4 and ' ' in ctx.message.content:
        type = ctx.message.content.split()[1]
    print('{0.author} requested a '.format(ctx.message) + type + ' joke.')
    joke = helper.get_joke(type)
    for j in joke:
        if len(j) > 0:
            print(j)
            await ctx.send(j)
            time.sleep(2)

@bot.command(name='gif', help='Gets a GIF')
async def gif(ctx):
    search_term = ''
    if len(ctx.message.content) > 3 and ' ' in ctx.message.content:
        search_term = ctx.message.content.split()[1]
        if len(ctx.message.content.split()) >= 3 and ctx.message.content.split()[2].isnumeric():
            limit = int(ctx.message.content.split()[2])
        else:
            limit = 1
    print('{0.author} requested a '.format(ctx.message) + search_term + ' gif.')
    gif = helper.get_gif(search_term, limit)

    for g in gif:
        if len(g) > 0:
            print(g)
            await ctx.send(g)
            time.sleep(1)

@bot.command(name='menme', help='Mentions the user issuing the command')
async def menme(ctx):
    await ctx.send('<@' + str(ctx.message.author.id) + '>')

@bot.command(name='menchan', help='Mentions the channel the issuing command comes from')
async def menchan(ctx):
    await ctx.send('<#' + str(ctx.message.channel.id) + '>')

@bot.command(name='message', help='Sends a message as Ni-Man to a specified channel.')
async def message(ctx):
    channel = ctx.message.channel_mentions[0]
    if len(ctx.message.content.split('\"')) >= 2:
        await channel.send(ctx.message.content.split('\"')[1])

# Admin Commands
@bot.command(name='admin', help='It\'s a secret LMAO')
async def admin(ctx):
    await ctx.message.delete()
    if ctx.message.author.name not in constants.admin_list:
        await ctx.message.channel.send('Sorry <@' + str(ctx.message.author.id) + '>, you do not have permission to use that command. Please see <@' + constants.user_Striker1521_0430 + '>')
        print(ctx.message.author.name + ' tried to run and admin command but it failed.')
        return
    command = ctx.message.content[ctx.message.content.find(constants.symbol + 'admin') + 7:]
    if not command:
        print('Command payload is empty')
        await ctx.send(content='Command Payload is empty.', delete_after=3)
    print(command)
    await helper.exec_command(command)
