import asyncio
import discord
from discord.ext import commands
from bot import roles


async def convert_kwargs(bot, *args):
    # storages = await bot.database.get_storages()
    storages = ['yellowjack']
    kwargs = {args[i].lower(): args[i + 1].lower() for i in range(0, len(args), 2)}
    cleaned = {}

    for key, value in kwargs.items():
        if key == 'priority':
            if value == 'true':
                cleaned[key] = 1
            elif value == 'false':
                cleaned[key] = 0
        elif key == 'amount':
            if value.isdigit():
                cleaned[key] = int(value)
        elif key == 'discount':
            if value.isdigit():
                cleaned[key] = int(value)

        elif key == 'storage':
            if value in storages:
                cleaned[key] = value

    return cleaned    


class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    @commands.has_role(roles['management_role']) 
    async def edit(self, ctx, *args):
        # Getting the order object
        order = await ctx.get_order()
        if order is None:
            return

        kwargs = await convert_kwargs(self.bot, *args)
        content = '\n'.join(f'-{key.title()}: {str(value).title()}' for key, value in kwargs.items())
        # Creating the embed
        embed = discord.Embed(title='Parameters edited', description=f'```{content}```', colour=discord.Colour.greyple())
        await ctx.send(embed=embed)
        # Editing the order with the options
        await order.edit(kwargs)
        
        pins = await ctx.channel.pins()
        message = pins[0]
        await message.edit(embed=order.embed)


    @commands.command()
    @commands.has_role(roles['management_role'])
    async def cancel(self, ctx):
        # Getting the order object 
        order = await ctx.get_order()
        if order is None:
            return

        await ctx.send(f'Cancelling **GS-{order.id}**...')
        # Getting the roles
        customer_role = discord.utils.get(ctx.guild.roles, name=f'GS-{order.id}')
        worker_role = discord.utils.get(ctx.guild.roles, name=f'GS-{order.id} worker')
        # Cancelling the order and deleting roles and channel
        await order.cancel()
        await customer_role.delete()
        await worker_role.delete()
        await ctx.channel.delete()

    

def setup(bot):
    bot.add_cog(Management(bot))