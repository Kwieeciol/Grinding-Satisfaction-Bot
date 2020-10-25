import discord
from discord.ext import commands
import resources.constants as constants

class Customers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def new(self, ctx):
        pass


def setup(client):
    client.add_cog(Customers(client))
