import re
import asyncio
import discord
import datetime
from .constants import proceed_message
from .database import fetch_order

__all__ = ['date', 'return_int', 'edit_embed', 'edit_progress', '_is_order_embed', '_is_proceed_embed', 'total_price']

def date():
    """Returns todays date

    Returns:
        [str]: Todays date
    """
    return datetime.datetime.now().strftime('%d.%m.%Y')


def return_int(s: str):
    """Returns all the digits in a string joined

    Args:
        s (str): The string in with to search the digits

    Returns:
        [int]: Digits
    """
    return int(''.join([l for l in s if l.isdigit()]))


def total_price(id: int):
    """Calculates the total price for the order

    Args:
        id (int): The order ID
    
    Returns:
        [str]: Total price separated by commas
    """
    # details = asyncio.get_event_loop().run_until_complete(fetch_order(id))
    pass


def edit_embed(embed: discord.Embed, options: dict):
    """Edits an embed with the specified options

    Args:
        embed (discord.embeds.Embed): The order embed to edit
        options (dict): The parameters to change

    Returns:
        [discord.Embed]: An embed with the new parameters changed
    """
    dct = embed.to_dict()
    fields = dct['fields']

    id = return_int(embed.title)
    new_price = total_price()

    for field in fields:
        name, value, _ = field.values()
        if name.lower() in options:
            field['value'] = options[name.lower()]

    return discord.Embed.from_dict(dct)


def edit_progress(embed: discord.Embed, progress: int):
    """Edits an embed progress

    Args:
        embed (discord.embeds.Embed): The order embed to edit
        progress (int): The progress to change

    Returns:
        [discord.Embed]: An embed with the new progress changed
    """
    dct = embed.to_dict()
    fields = dct['fields']
    for field in fields:
        name, value, _ = field.values()
        if name.lower() == 'progress':
            field['value'] = str(progress)
    
    return discord.Embed.from_dict(dct)


title_pattern = '\*GS-\d+\*'
author_pattern = '\w+#\d{4}'

def _is_order_embed(message: discord.Message):
    """Return True of the message contains an order embed

    Args:
        message (discord.Message): The message in which to check

    Returns:
        [discord.Embed/bool]: Order embed/False
    """
    try:
        embed = message.embeds[0]

        title = embed.title
        author = embed.author.name
        fields = embed.fields

        if bool(re.search(title_pattern, title)):
            # The title is good
            if bool(re.search(author_pattern, author)):
                # The author is good
                if len(fields) == 5 or len(fields) == 6:
                    return embed

        else:
            return False

    except Exception:
        return False


description_pattern = f'<:gs:\d+> {proceed_message}'

def _is_proceed_embed(message: discord.Message):
    """Checks if the message is a proceed embed

    Args:
        message (discord.Message): The message in which yo check

    Returns:
        [discord.Embed/bool]: The proceed embed or False
    """
    try:
        embed = message.embeds[0]

        description = embed.description

        if bool(re.search(description_pattern, description)):
            return embed

    except Exception:
        return False
