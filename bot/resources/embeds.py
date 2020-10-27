import discord
from .functions import date
from .constants import COLOUR

not_valid_channel = discord.Embed(description=':x: Please use this command in a valid channel', colour=discord.Colour.from_rgb(200, 0, 0))
not_valid_answer = discord.Embed(description=':x: Wrong answer, please try again.', colour=discord.Colour.from_rgb(200, 0, 0))
cancelled_command = discord.Embed(description=':x: Cancelled command.', colour=discord.Colour.from_rgb(200, 0, 0))


def customer_embed_1(ctx):
    embed = discord.Embed(title='What is your in-game ID?', colour=COLOUR)
    embed.add_field(name='\u200b', value=f"{ctx.author}\nType 'cancel' to cancel the order process. • {date()}")
    embed.set_author(name=f'Customer details', icon_url=ctx.guild.icon_url)
    return embed

def customer_embed_2(ctx):
    embed = discord.Embed(title='What is your in-game name?', colour=COLOUR)
    embed.add_field(name='\u200b', value=f"{ctx.author}\nType 'cancel' to cancel the order process. • {date()}")
    embed.set_author(name='Custome details', icon_url=ctx.guild.icon_url)
    return embed

def order_embed_1(ctx, items):
    message = '   {:19s} Price Each\n{}\n'.format('Item', '-'*30)
    for num, item in enumerate(items.items()):
        item, value = item
        string = '{:d}. {:20s} ${:,}'.format(num+1, item.title(), int(value[0]))
        message = message + string + '\n'

    embed = discord.Embed(title='What would you like to order?', description=f'```{message}```\nThe displayed prices are per **one** item.', colour=COLOUR)
    embed.add_field(name='\u200b', value=f"{ctx.author}\nType 'cancel' to cancel the order process. • {date()}")
    embed.set_author(name=f'Order details', icon_url=ctx.guild.icon_url)
    return embed

def order_embed_2(ctx, item, limit):
    embed = discord.Embed(title='What amount would you like to order?', description=f"The order limit for **{item}** is **{limit}**.\nYou must stay within the order!", colour=COLOUR)
    embed.add_field(name='\u200b', value=f"{ctx.author}\nType 'cancel' to cancel the order process. • {date()}")
    embed.set_author(name=f'Order details', icon_url=ctx.guild.icon_url)
    return embed

def order_embed_3(ctx, storages):
    message = '   {:20s} Fee\n{}\n'.format('Storage', '-'*30)
    for num, storage in enumerate(storages.items()):
        storage, value = storages
        string = '{}{:20s} ${:,}'.format(storage.title(), value[-1])
        message = message + string + '\n'

    embed = discord.Embed(title='In what storage would you like it to be stored?', description=f"```{message}```", colour=COLOUR)
    embed.add_field(name='\u200b', value=f"{ctx.author}\nType 'cancel' to cancel the order process. • {date()}")
    embed.set_author(name=f'Order details', icon_url=ctx.guild.icon_url)
    return embed
