import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.reactions = True

client = commands.Bot(command_prefix='!', intents=intents)
TOKEN = os.getenv('TOKEN')


@client.event
async def on_ready():
    print('Bot is ready')
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name='Transport Tycoon'))


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! `{round(client.latency * 1000)}ms`')


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    def check(m):
        return not m.pinned
    await ctx.channel.purge(limit=amount+1)


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} loaded')


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} unloaded')


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} reloaded')


for filename in os.listdir('./bot/cogs'):
    if filename.endswith('.py') and filename != '__init__.py':
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'{filename[:-3]} loaded')


@client.event
async def on_command_error(ctx, error):
    print(type(error), error)


client.run(TOKEN)
