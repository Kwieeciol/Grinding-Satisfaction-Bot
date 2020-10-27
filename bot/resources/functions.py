import re
import discord
import datetime
from .constants import proceed_message

__all__ = ['date', 'return_int', 'edit_embed', 'edit_progress', '_is_order_embed', '_is_proceed_embed', 'total_price']

def date():
    return datetime.datetime.now().strftime('%d.%m.%Y')


def return_int(s: str):
    return int(''.join([l for l in s if l.isdigit()]))


def edit_embed(embed, options):
    dct = embed.to_dict()
    fields = dct['fields']
    for field in fields:
        name, value, _ = field.values()
        if name.lower() in options:
            field['value'] = options[name.lower()]

    return discord.Embed.from_dict(dct)


def edit_progress(embed, progress):
    dct = embed.to_dict()
    fields = dct['fields']
    for field in fields:
        name, value, _ = field.values()
        if name.lower() == 'progress':
            field['value'] = str(progress)


title_pattern = '\*GS-\d+\*'
author_pattern = '\w+#\d{4}'

def _is_order_embed(message):
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

def _is_proceed_embed(message):
    try:
        embed = message.embeds[0]

        description = embed.description

        if bool(re.search(description_pattern, description)):
            return embed

    except Exception:
        return False


def total_price(amount: int, price_each: int, storage_fee: int, discount: int=0, priority: bool=False):
    item_price = amount * price_each
    total_storage_fee = amount * storage_fee

    total_price = item_price + total_storage_fee

    if discount:
        total_price = round(total_price * (1 - (discount / 100)))

    if priority:
        total_price = round(total_price * 1.25)

    return total_price