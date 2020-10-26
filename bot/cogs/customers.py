import datetime
import discord
from discord.ext import commands
import resources.constants as constants
import resources.database as database
import resources.embeds as embeds

def check_limit(amount, limit):
    if amount.isdigit():
        if int(amount) <= limit:
            return True
        else:
            return False
    else:
        return False


class Customers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def order(self, ctx):
        channel = self.client.get_channel(constants.Channels.queued)
        embed = discord.Embed(title='*GS-1*', colour=discord.Colour.purple())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(name='Cargo', value='Sand', inline=True)
        embed.add_field(name='Amount', value='10000', inline=True)
        embed.add_field(name='Storage', value='Yellowjack', inline=True)
        embed.add_field(name='Priority', value='False', inline=True)
        embed.add_field(name='Total Price', value='$130,000,000', inline=True)
        message = await channel.send(embed=embed)
        await message.add_reaction('✅')


    @commands.command()
    async def new(self, ctx):
        def check(m):
            if m.guild == None and m.content.lower() == 'cancel':
                raise KeyError('Cancelled command')
            return m.guild == None and m.author == ctx.author

        # Checking if the customer exists
        customer = await database.check_customer(ctx.author.id)

        if not customer:
            await ctx.author.send(embed=embeds.customer_embed_1(ctx))
            tycoon_id = await self.client.wait_for('message', check=check)
            # Making sure the tycoon ID is an integer
            while not tycoon_id.content.isdigit():
                await ctx.author.send(embed=embeds.not_valid_answer)
                tycoon_id = await self.client.wait_for('message', check=check)

            await ctx.author.send(embed=embeds.customer_embed_2(ctx))
            tycoon_name = await self.client.wait_for('message', check=check)
            # Addind the non-existing customer to the database
            customer_data = {'name': ctx.author.name,
                            'discord_id': ctx.author.id,
                            'tycoon_name': tycoon_name.content,
                            'tycoon_id': int(tycoon_id.content)}

            await database.new_customer(customer_data)
        # Fetching the items from the database
        items = await database.items()

        await ctx.author.send(embed=embeds.order_embed_1(ctx, items))
        item = await self.client.wait_for('message', check=check)
        # Checking if the item is valid
        while not item.content.lower() in items:
            await ctx.author.send(embed=embeds.not_valid_answer)
            item = await self.client.wait_for('message', check=check)
        # Getting the price each and limit of the item
        price, limit = items[item.content.lower()]

        await ctx.author.send(embed=embeds.order_embed_2(ctx, item.content, limit))
        amount = await self.client.wait_for('message', check=check)
        # Checking if the amount is valid
        while not check_limit(amount.content, limit):
            await ctx.author.send(embed=embeds.not_valid_answer)
            amount = await self.client.wait_for('message', check=check)

        # Fetching the available storages
        storages = await database.storages()
        await ctx.author.send(embed=embeds.order_embed_3(ctx, storages))


def setup(client):
    client.add_cog(Customers(client))
