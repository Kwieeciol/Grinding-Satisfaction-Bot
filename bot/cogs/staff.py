import discord
from discord import PermissionOverwrite
from discord.ext import commands
from resources.constants import Channels, Categories, MODERATION_ROLES, STAFF_ROLES, COLOUR, proceed_message, EMOJI_ID
import resources.database as database
from resources.functions import return_int, edit_progress, _is_order_embed, _is_proceed_embed


def _check_order(option, embed):
    fields = embed.to_dict()['fields']
    progress = limit = 0

    for field in fields:
        name, value, _ = field.values()
        if name == 'Amount':
            limit = int(value)
        elif name == 'Progress':
            progress = int(value)

    if option == 'progress':
        if progress <= limit:
            return True
        return False
    
    elif option == 'limit':
        if progress == limit:
            return True
        return False


class Staff(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def proceed(self, ctx):
        emote = discord.utils.get(ctx.guild.emojis, id=EMOJI_ID)
        message = await ctx.send(embed=discord.Embed(description=f'{emote} {proceed_message}', colour=COLOUR))
        await message.add_reaction('✅')
        await message.add_reaction('❌')


    async def cancel_proceed(self, ctx):
        # Deleting the 'proceed' message
        await ctx.message.delete()
        # Getting the pinned message
        pins = await ctx.channel.pins()
        message = pins[0]

        await message.clear_reactions()
        await message.add_reaction('✅')


    async def take_order(self, ctx):
        if (embed := _is_order_embed(ctx.message)):
            id = return_int(embed.title)
            print(embed.to_dict())
            # Getting the roles
            customer_role = discord.utils.get(ctx.guild.roles, name=f'GS-{id}')
            worker_role = discord.utils.get(ctx.guild.roles, name=f'GS-{id} worker')
            management_role = discord.utils.get(ctx.guild.roles, id=MODERATION_ROLES)
            # The channel permissions overwrites
            overwrites = {
                ctx.guild.default_role: PermissionOverwrite(read_messages=False),
                customer_role: PermissionOverwrite(read_messages=True, send_messages=False),
                worker_role: PermissionOverwrite(read_messages=True, send_messages=True),
                management_role: PermissionOverwrite(read_messages=True, send_messages=True)
            }

            category = discord.utils.get(ctx.guild.categories, id=Categories.in_progress)
            # Channel creation
            order_channel = await ctx.guild.create_text_channel(f'GS-{id}', overwrites=overwrites, category=category)
            # Adding the roles
            await ctx.author.add_roles(worker_role)
            # Updating the embed with a new field - 'Progress', sending and pinning it
            embed.add_field(name='Progress', value='0', inline=True)
            message = await order_channel.send(embed=embed)
            await message.pin()
            await message.add_reaction('✅')
            # Deleting the old message
            await ctx.message.delete()
            # Assigning the order to the worker in the database
            # await database.assign_order(id, ctx.author.id)


    async def change_status(self, ctx):
        def check(m):
            return not m.pinned

        pins = await ctx.channel.pins()
        message = pins[0]
        embed = message.embeds[0]

        id = return_int(embed.title)

        customer_role = discord.utils.get(ctx.guild.roles, name=f'GS-{id}')
        worker_role = discord.utils.get(ctx.guild.roles, name=f'GS-{id} worker')
        management_role = discord.utils.get(ctx.guild.roles, id=MODERATION_ROLES)
        # Getting the customer
        customer = [member for member in ctx.guild.members for role in member.roles if role.name == f'GS-{id}'][0]
        # Getting the new category
        category = discord.utils.get(ctx.guild.categories, id=Categories.pending_collection)
        # Deleting messages apart from pinned ones
        await ctx.channel.purge(limit=100, check=check)

        overwrites = {
            ctx.guild.default_role: PermissionOverwrite(read_messages=False),
            customer_role: PermissionOverwrite(read_messages=True, send_messages=False),
            worker_role: PermissionOverwrite(read_messages=True, send_messages=False),
            management_role: PermissionOverwrite(read_messages=True, send_messages=True)
        }
        # Editing the category and overwrites
        await ctx.channel.edit(category=category, overwrites=overwrites)
        await message.clear_reactions()
        await message.add_reaction('✅')
        # Sending the final message
        await ctx.send(f'Hi, {customer.mention}! Your order **GS-{id}** is ready to be collected! Please contact {ctx.author.mention} for collection timings')
        # Changing the order to 'pending-collection' status in the database
        # await database.collection(id)


    async def finish_order(self, ctx):
        # Getting the embed
        pins = await ctx.channel.pins()
        embed = pins[0].embeds[0]

        id = return_int(embed.title)
        # Deleting the channel
        await ctx.channel.delete()
        # Getting the roles
        customer_role = discord.utils.get(ctx.guild.roles, name=f'GS-{id}')
        worker_role = discord.utils.get(ctx.guild.roles, name=f'GS-{id} worker')
        # Deleting the roles
        await customer_role.delete()
        await worker_role.delete()
        # Changing the order to 'completed' status in the database
        # await database.completed(id)


    async def _finish_order(self, ctx):
        emote = discord.utils.get(ctx.guild.emojis, id=EMOJI_ID)
        await ctx.send(embed=discord.Embed(description=f'{emote} Please, finish the order before you change the status.', colour=COLOUR))

        pins = await ctx.channel.pins()
        message = pins[0]

        await message.clear_reactions()
        await message.add_reaction('✅')


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.client.user.id:
            if payload.emoji.name == '✅':
                channel = self.client.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                author = channel.guild.get_member(payload.user_id)

                ctx = await self.client.get_context(message)
                ctx.author = author

                if channel.id == Channels.queued:
                    # The reaction has been added in the 'queued' channel
                    await self.take_order(ctx)

                elif channel.category != None:
                    if channel.category.id == Categories.in_progress:
                        # The reaction has been added in an order with 'in-progress' status
                        # Checking if the reacted message is an order or proceed embed
                        if (embed := _is_order_embed(message)):
                            if _check_order('limit', embed):
                                await self.proceed(ctx)

                            else:
                                await self._finish_order(ctx)

                        elif _is_proceed_embed(message):
                            await self.change_status(ctx)

                    elif channel.category.id == Categories.pending_collection:
                        # The reaction has been added in an order with 'pending-collection' status
                        if _is_order_embed(message):
                            await self.proceed(ctx)

                        elif _is_proceed_embed(message):
                            await self.finish_order(ctx)

            elif payload.emoji.name == '❌':
                channel = self.client.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)

                ctx = await self.client.get_context(message)

                if (category := channel.category) != None:
                    if category.id == Categories.in_progress or category.id == Categories.pending_collection:
                        if _is_proceed_embed(message):
                            await self.cancel_proceed(ctx)



    @commands.command(aliases=['p'])
    @commands.has_role(STAFF_ROLES)
    async def progress(self, ctx, amount: int):
        if (category := ctx.channel.category) != None:
            if category.id == Categories.in_progress:
                # Getting the message
                pins = await ctx.channel.pins()
                message = pins[0]
                embed = message.embeds[0]
                # Editing the embed
                embed = edit_progress(embed, amount)
                if _check_order('progress', embed):
                    emote = discord.utils.get(ctx.guild.emojis, id=EMOJI_ID)
                    id = return_int(ctx.channel.name)
                    await ctx.send(embed=discord.Embed(description=f'{emote} Changed progress of **GS-{id}** to **{amount}**', colour=COLOUR))
                    await message.edit(embed=embed)
                    # await database.set_progress(id, amount)

                else:
                    await ctx.send('Progress cannot exceed the limit.')


def setup(client):
    client.add_cog(Staff(client))
