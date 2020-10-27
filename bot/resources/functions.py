import re
import datetime

__all__ = ['date', 'return_int', '_is_order_embed']

def date():
    return datetime.datetime.now().strftime('%d.%m.%Y')


def return_int(s: str):
    return int(''.join([l for l in s if l.isdigit()]))


title_pattern = '\*GS-\d+\*'
author_pattern = '\w+#\d{4}'

def _is_order_embed(message):
    try:
        embed = message.embeds[0]

        title = embed.title
        author = embed.author
        fields = embed.fields

        if bool(re.search(title_pattern, title)):
            # The title is good
            if bool(re.search(author_pattern, author)):
                # The author is good
                if len(fields) == 5 or len(fields) == 6:
                    return True

        else:
            return False

    except Exception:
        return False
