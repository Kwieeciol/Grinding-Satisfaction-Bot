import discord

__all__ = ['Categories', 'Channels', 'MODERATION_ROLES', 'STAFF_ROLES', 'URL', 'COLOUR', 'proceed_message', 'EMOJI_ID']

class Categories:
    pending_collection = 740923676115075132
    in_progress = 740923709568843848

class Channels:
    lounge = 770992341586280518
    queued = 740951313482907748
    bot_commands = 745939379683590168
    log = 771335478372204575
    webhook = 771796441411747841
    lottery = 772182443800526858

class Roles:
    management = 741244092067086356
    staff = 713354499254648882
    customer = 769869836175933472

proceed_message = 'Are you sure you want to proceed?'

MODERATION_ROLES = Roles.management
STAFF_ROLES = Roles.staff

URL = 'http://grindingsatisfaction.herokuapp.com'

COLOUR = discord.Colour.purple()
EMOJI_ID = 745358651967012994