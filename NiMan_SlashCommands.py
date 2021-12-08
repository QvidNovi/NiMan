import requests
import discord
from discord_slash import SlashCommand, SlashContext

# Custom
import NiMan_Constants as constants
import NiMan_START as main

global slash
slash = main.slash

global guilds
guilds = [constants.GuildId]

def setup(bot):
    print('Setting up slash commands')

@slash.slash(name='test', guild_ids=guilds)
async def _test(ctx: SlashContext):
    await main.test(ctx)

@slash.slash(name='getuserid', guild_ids=guilds)
async def _getuserid(ctx: SlashContext):
    await main.getuserid(ctx)

@slash.slash(name='getchanid', guild_ids=guilds)
async def _getchanid(ctx: SlashContext):
    await main.getchanid(ctx)

@slash.slash(name='getguildid', guild_ids=guilds)
async def _getguildid(ctx: SlashContext):
    await main.getguildid(ctx)

@slash.slash(name='purge', guild_ids=guilds)
async def _purge(ctx: SlashContext):
    await main.purge(ctx)
