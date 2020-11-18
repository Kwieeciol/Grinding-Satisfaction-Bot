import discord
from discord.ext import commands
from resources.constants import COLOUR
from resources.database import fetch_items, fetch_storages


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Owner(bot))