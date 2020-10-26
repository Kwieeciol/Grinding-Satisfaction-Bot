import discord
from discord import PermissionOverwrite
from discord.ext import commands
from resources.constants import Channels, Categories, MODERATION_ROLES, STAFF_ROLES
import resources.database as database
from resources.functions import return_int

def _is_embed(message):
    try:
        return message.embeds[0]
    except Exception:
        return False


class Staff(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def take_order(self, ctx):
        if (embed := _is_embed(ctx.message)):
            id = return_int(embed.title)
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
            # Deleting the old message
            await ctx.message.delete()
            # Assigning the order to the worker in the database
            # await database.assign_order(id, ctx.author.id)


    async def change_status(self, ctx):
        # --to do--
        # 1. Check if the reacted message is an embed
        # 2. Check if the progress is the same as the ordered amount
        # 3. Ask the worker if he sure he want to procedure
        # 4. Move the channel to 'pending-collection' category
        # 5. Change the permissions for the worker role to: send_messages = False
        # 6. Remove the reactions in the embed
        # 7. Delete all the messages apart from the pinned ones (embed)
        pass


    async def finish_order(self, ctx):
        # --to do--
        # 1. Check if the reacted message is an embed
        # 2. Delete the channel and roles
        # 3. Change the status of the order in the database to 'completed'
        pass


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.client.user.id:
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
                    pass

                elif channel.category.id == Categories.pending_collection:
                    # The reaction has been added in an order with 'pending-collection' status
                    pass


    @commands.command(aliases=['p'])
    @commands.has_role(STAFF_ROLES)
    async def progress(self, ctx, amount: int):
        if (category := ctx.channel.category) != None:
            if category.id == Categories.in_progress:
                # --to do--
                # 1. Fetch the embed
                # 2. Get the details of the order
                # 3. Check if the progress is less than the amount ordered
                # 4. Edit the embed with the new progress`
                # 5. Edit the database
                pass


def setup(client):
    client.add_cog(Staff(client))
