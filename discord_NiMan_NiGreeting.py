import discord
from datetime import datetime

client = discord.Client()

global Token
Token = 'ODI0MzM3MjU4MjQwOTMzOTI5.YFt55Q.8ReNKiJsR2gWt-qPv-QdC-br8HM'

guild_index = 0
channel_index = 2
#general = 2
#bot-tester = 4

message = 'G\'day ni'

current_time = datetime.now().strftime("%H:%M:%S")
current_hour = int(datetime.now().strftime("%H"))

if current_hour >= 0 and current_hour <= 4:
    message = 'It\'s way to early, go to sleep ni :sleeping:'
elif current_hour > 4 and current_hour <= 11:
    message = 'G\'morning ni :angel:'
elif current_hour > 11 and current_hour <= 12:
    message = 'Happy noon ni'
elif current_hour > 12 and current_hour <= 16:
    message = 'Good afternoon ni'
elif current_hour > 16 and current_hour <= 19:
    message = 'Have a nice evening ni'
elif current_hour > 19 and current_hour < 24:
    message = 'G\'night all of you ni\'s, see you 2morow :smiling_face_with_3_hearts:'

@client.event
async def on_ready():
    print('Logged in as {0.user.name} at '.format(client) + current_time)
    if client.guilds[guild_index] and client.guilds[guild_index].channels[channel_index]:
        await client.guilds[guild_index].channels[channel_index].send(message)
    else:
        print('Failed to send message')
    await client.logout()

client.run(Token)
