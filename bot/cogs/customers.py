import datetime
import discord
from discord.ext import commands
import resources.constants as constants
from resources.constants import COLOUR, EMOJI_ID
import resources.database as database
import resources.embeds as embeds


def _check_limit(amount, limit):
    if amount.isdigit():
        if int(amount) <= limit:
            return True
    return False


def _storage_check(storage, storages):
    if storage.content.lower() in storages:
        return True
    # if storage.content.isdigit():
    #     if int(storage) in len(storages):
    #         return True
    return False


class Customers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emote = f'<:gs:{EMOJI_ID}>'


    @commands.command()
    async def order(self, ctx):
        channel = self.bot.get_channel(constants.Channels.queued)
        embed = discord.Embed(title='*GS-1*', colour=COLOUR)
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
            if m.content.lower() == 'cancel':
                raise KeyError('Cancelled command')
            return m.guild == None and m.author == ctx.author
        
    # Checking if the customer exists in the database
        customer = await database.check_customer(ctx.author.id)

        if not customer:
            # Tycoon ID
            await ctx.author.send(embed=embeds.customer_embed_1(ctx))
            tycoon_id = await self.bot.wait_for('message', check=check)
            # Making sure the message is a digit
            while not tycoon_id.content.isdigit():
                await ctx.author.send(embed=embeds.not_valid_answer)
                tycoon_id = await self.bot.wait_for('message', check=check)
            # Tycoon name
            await ctx.author.send(embed=embeds.customer_embed_2(ctx))
            tycoon_name = await self.bot.wait_for('message', check=check)
            # Adding the customer to the database
            customer_data = {
                'name': ctx.author.name,
                'discord_id': ctx.author.id,
                'tycoon_name': tycoon_name.content,
                'tycoon_id': int(tycoon_id.content)
            }
            await database.new_customer(customer_data)
        
        # Fetching the items and storages
        items = await database.fetch_items()
        storages = await database.fetch_storages()
        # Item
        await ctx.author.send(embed=embeds.order_embed_1(ctx, items))
        item = await self.bot.wait_for('message', check=check)
        # Checking if the item is valid
        while not item.content.lower() in items:
            await ctx.author.send(embed=embeds.not_valid_answer)
            item = await self.bot.wait_for('message', check=check)
        
        _, price_each, limit = items[item.content.lower()].values()
        # Amount
        await ctx.author.send(embed=embeds.order_embed_2(ctx, item.content, limit))
        amount = await self.bot.wait_for('message', check=check)
        # Checking if the amount is valid
        while not _check_limit(amount.content, limit):
            await ctx.author.send(embed=embeds.not_valid_answer)
            amount = await self.bot.wait_for('message', check=check)
        # Storage
        await ctx.author.send(embed=embeds.order_embed_3(ctx, storages))
        storage = await self.bot.wait_for('message', check=check)
        # Checking if the chsoen storage is valid
        while not _storage_check(storage, storages):
            await ctx.author.send(embed=embeds.not_valid_answer)
            storage = await self.bot.wait_for('message', check=check)
        storage_id, storage_fee = storages[storage.content.lower()].values()
        # Priority
        await ctx.author.send(embed=embeds.order_embed_4(ctx))
        priority = await self.bot.wait_for('message', check=check)

        if priority.content.lower() in ['yes', 'ye', 'y']:
            priority = 1
        else:
            priority = 0

        order_data = {
            'priority': priority,
            'discord_id': ctx.author.id,
            'product_name': item.content.lower(),
            'price_each': price_each,
            'amount': int(amount.content),
            'storage_id': storage_id
        }


def setup(bot):
    bot.add_cog(Customers(bot))
