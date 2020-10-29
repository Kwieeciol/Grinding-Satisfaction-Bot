import asyncio
import discord
from discord.ext import commands
import resources.database as database
from resources.functions import return_int, edit_embed
from resources.constants import MODERATION_ROLES, COLOUR, EMOJI_ID, Categories


def convert_args(args):
    available_options = ['amount', 'storage', 'discount', 'priority']

    if len(args) % 2 == 0:
        kwargs = {}
        for x in range(0, len(args), 2):
            kwargs[args[x].lower()] = args[x + 1]

        kwargs = {key: value for key, value in kwargs.items() if key in available_options}
        return kwargs

    return False


class Management(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_any_role(*MODERATION_ROLES)
    async def edit(self, ctx, *args):
        emote = discord.utils.get(ctx.guild.emojis, id=EMOJI_ID)
        if (category := ctx.channel.category):
            if category.id == Categories.in_progress:
                if (options := convert_args(args)):
                    is_true = all([True if value.isdigit() else False for value in options.values()])
                    if is_true:
                        # Getting the message and editing it with the new embed
                        pins = await ctx.channel.pins()
                        message = pins[0]
                        embed = message.embeds[0]
                        await ctx.send(embed=discord.Embed(description=f'{emote} Please wait... Editing the order.', colour=COLOUR))

                        id = return_int(embed.title)
                        # Editing the database
                        # await database.edit(id, data=options)

                        # new_embed = edit_embed(embed, options)

                        # await message.edit(embed=new_embed)
                    else:
                        await ctx.send(embed=discord.Embed(description=f'{emote} Please use only digits.', colour=COLOUR))
                else:
                    await ctx.send(embed=discord.Embed(description=f'{emote} Please use valid arguments **(priority, amount, storage, discount)**', colour=COLOUR))
            else:
                await ctx.send(embed=discord.Embed(description=f'{emote} Please use this command in a valid channel.', colour=COLOUR))
        else:
            await ctx.send(embed=discord.Embed(description=f'{emote} Please use this command in a valid channel.', colour=COLOUR))


    @commands.command()
    @commands.has_any_role(*MODERATION_ROLES)
    async def cancel(self, ctx):
        def check(emoji, author):
            return str(emoji) == '✅' and author == ctx.author

        emote = discord.utils.get(ctx.guild.emojis, id=EMOJI_ID)
        if (category := ctx.channel.category) != None:
            if category.id == Categories.in_progress:
                # ID of the order
                id = return_int(ctx.channel.name)

                message = await ctx.send(embed=discord.Embed(description=f'{emote} Are you sure you want to cancel **GS-{id}**?', colour=COLOUR))
                await message.add_reaction('✅')
                await message.add_reaction('❌')

                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

                    customer_role = discord.utils.get(ctx.guild.roles, name=f'GS-{id}')
                    worker_role =  discord.utils.get(ctx.guild.roles, name=f'GS-{id} worker')
                    # Creating an cancel embed
                    embed = discord.Embed(description=f'{emote} Hi! **GS-{id}** has been **cancelled**.', colour=COLOUR)
                    # Getting the worker
                    worker = [member for member in ctx.guild.members for role in member.roles if role == worker_role][0]
                    await worker.send(embed=embed)
                    # Getting the customer
                    customer = [member for member in ctx.guild.members for role in member.roles if role == customer_role][0]
                    await customer.send(embed=embed)
                    # Deleting the channel and roles
                    await ctx.channel.delete()

                    await customer_role.delete()
                    await worker_role.delete()
                    # Canceling the order in the database
                    await database.cancel(id)

                except asyncio.TimeoutError:
                    await message.delete()

                else:
                    await message.delete()
            else:
                await ctx.send(embed=discord.Embed(description=f'{emote} Please use this command in a valid channel.', colour=COLOUR))
        else:
            await ctx.send(embed=discord.Embed(description=f'{emote} Please use this command in a valid channel.', colour=COLOUR))


def setup(client):
    client.add_cog(Management(client))