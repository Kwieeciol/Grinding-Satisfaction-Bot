import discord
from discord.ext import commands
import resources.constants as constants
import resources.database as database

class Customers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def new(self, ctx):
        print(await database.check_customer(ctx.author.id))


def setup(client):
    client.add_cog(Customers(client))
