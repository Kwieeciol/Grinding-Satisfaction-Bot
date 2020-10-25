__all__ = ['Categories', 'Channels', 'MODERATION_ROLES', 'STAFF_ROLES']

class Categories:
    pending_collection = 740923676115075132
    in_progress = 740923709568843848

class Channels:
    queued = 740951313482907748
    bot_commands = 745939379683590168

class Roles:
    management = 741244092067086356
    staff = 713354499254648882
    customer = 769869836175933472

MODERATION_ROLES = Roles.management
STAFF_ROLES = Roles.staff
