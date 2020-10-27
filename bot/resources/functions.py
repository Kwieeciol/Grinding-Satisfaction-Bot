import re
import discord
import datetime

__all__ = ['date', 'return_int', 'edit_embed', '_is_order_embed', '_is_proceed_embed']

def date():
    return datetime.datetime.now().strftime('%d.%m.%Y')


def return_int(s: str):
    return int(''.join([l for l in s if l.isdigit()]))


def edit_embed(embed, **options):
    dct = embed.to_dict()
    fields = dct['fields']
    for field in fields:
        name, value, _ = field.values()
        if name.lower() in options:
            field['value'] = options[name.lower()]

    return discord.Embed.from_dict(dct)


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


def _is_proceed_embed(message):
    # Finish the function, find a pattern
    pass
