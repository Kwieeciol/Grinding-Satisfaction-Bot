import os
import asyncio
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from resources.constants import Channels, COLOUR, EMOJI_ID
from resources.database import session


load_dotenv()


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


intents = discord.Intents.default()
intents.reactions = True
intents.members = True
intents.messages = True
intents.emojis = True


client = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True, owner_ids=[675002733056622592, 610403762976063489])
TOKEN = os.getenv('TOKEN')


@client.event
async def on_ready():
    print('Bot is ready')
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name='Transport Tycoon'))


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
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'{filename[:-3]} loaded')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(embed=discord.Embed(description=f'{emote} Command does not exist.', colour=COLOUR))
    
    elif isinstance(error, discord.ext.commands.errors.NotOwner):
        await ctx.send(embed=discord.Embed(description=f'<:gs:{EMOJI_ID}> Command does not exist.', colour=COLOUR))
    
    elif isinstance(error, discord.ext.commands.errors.MissingRole):
        await ctx.send(embed=discord.Embed(description=f'<:gs:{EMOJI_ID}> Command does not exist.', colour=COLOUR))

    else:
        if ctx.guild != None:
            channel = discord.utils.get(ctx.guild.channels, id=Channels.log)
            embed = discord.Embed(title=str(type(error)), description=f'```{error}```', colour=discord.Colour.gold())
            embed.add_field(name='Content:', value=f'{ctx.message.content} | **{str(ctx.author)} ({ctx.author.id})**', inline=False)
            embed.add_field(name='URL:', value=ctx.message.jump_url, inline=False)
            await channel.send(embed=embed)
        else:
            print(type(error), error)


@client.event
async def on_disconnect():
    await session.close()


if __name__ == '__main__':
    client.run(TOKEN)
