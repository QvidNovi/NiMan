import discord
from discord.ext import commands,tasks
from discord_slash import SlashCommand, SlashContext
import json
import threading
import time
import os
import multiprocessing
import random
import requests

# Custom
import NiMan_Constants as constants
import NiMan_Helper as helper

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=constants.symbol, intents=intents)
slash = SlashCommand(bot)

bot.load_extension("NiMan_Commands")
bot.load_extension("NiMan_SlashCommands")
print('--')

# Events
@bot.event
async def on_ready():
    print('Logged in as {0.user.name}'.format(bot))
    await bot.change_presence(activity=discord.Game('The Skin Flute'))
    print('Changed presence.')
    print('Ready')
    print('--')


@bot.event
async def on_message(message):
    if (await helper.process_message(message, bot)):
        return
    await bot.process_commands(message)

bot.run(constants.Token)
