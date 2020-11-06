import discord
from discord.ext import commands
from resources.constants import COLOUR
from resources.database import fetch_items, fetch_storages


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Owner(client))