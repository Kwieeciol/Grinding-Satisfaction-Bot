import discord
from discord import PermissionOverwrite
from discord.ext import commands
from resources.constants import Channels, Categories, MODERATION_ROLES
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

    async def take_order(self, payload, channel):
        message = await channel.fetch_message(payload.message_id)
        user = discord.utils.get(channel.guild.members, id=payload.user_id)
        if (embed := _is_embed(message)):
            id = return_int(embed.title)
            # Getting the roles
            customer_role = discord.utils.get(channel.guild.roles, name=f'GS-{id}')
            worker_role = discord.utils.get(channel.guild.roles, name=f'GS-{id} worker')
            management_role = discord.utils.get(channel.guild.roles, id=MODERATION_ROLES)
            # The channel permissions overwrites
            overwrites = {
                channel.guild.default_role: PermissionOverwrite(read_messages=False),
                customer_role: PermissionOverwrite(read_messages=True, send_messages=False),
                worker_role: PermissionOverwrite(read_messages=True, send_messages=True),
                management_role: PermissionOverwrite(read_messages=True, send_messages=True)
            }

            category = discord.utils.get(channel.guild.categories, id=Categories.in_progress)
            # Channel creation
            order_channel = await channel.guild.create_text_channel(f'GS-{id}', overwrites=overwrites, category=category)
            # Updating the embed with a new field - 'Progress'
            embed.add_field(name='Progress', value='0', inline=True)
            # Sending the embed and pinning it
            channel_message = await order_channel.send(embed=embed)
            await channel_message.pin()
            # Deleting the old message
            await message.delete()
            await user.add_roles(worker_role)
            # Assigning the order to the worker in the database
            await database.assign_order(id, user.id)



    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.client.get_channel(payload.channel_id)
        if payload.user_id != self.client.user.id:
            if channel.id == Channels.queued:
                # The reaction has been added in the 'queued' channel
                await self.take_order(payload, channel)

            elif channel.category != None:
                if channel.category.id == Categories.in_progress:
                    # The reaction has been added in an order with 'in-progress' status
                    pass

                elif channel.category.id == Categories.pending_collection:
                    # The reaction has been added in an order with 'pending-collection' status
                    pass


def setup(client):
    client.add_cog(Staff(client))
