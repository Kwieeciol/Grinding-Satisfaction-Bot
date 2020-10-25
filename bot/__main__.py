import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix='!')
TOKEN = os.getenv('TOKEN')


@client.event
async def on_ready():
    print('Bot is ready')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! `{round(client.latency * 1000)}ms`')


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



client.run(TOKEN)
