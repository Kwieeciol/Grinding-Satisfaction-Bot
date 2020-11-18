import os
import asyncio
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from resources.constants import Channels, COLOUR, EMOJI_ID
from resources.database import session


# Setting up the logging module
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Intents
intents = discord.Intents.default()
intents.members = True

# Creating the bot instance
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True, owner_ids=[675002733056622592, 610403762976063489])


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    await bot.wait_until_ready()
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name='Transport Tycoon'))
    # Loading Cogs
    for filename in os.listdir('./bot/cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'{filename[:-3]} loaded')



@bot.command()
async def ping(ctx):
    """Command for checking latency between a HEARTBEAT and a HEARTBEAT_ACK in miliseconds."""
    await ctx.send(f'Pong! `{round(bot.latency * 1000)}ms`')


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    """Command for loading a cog"""
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} loaded')


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    """Command for unloading a cog"""
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} unloaded')


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    """Command for reloading a cog"""
    bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} reloaded')


if __name__ == '__main__':
    load_dotenv()
    bot.run(os.getenv('TOKEN'))
