import discord
from discord.ext import commands
from resources.constants import Channels, Categories
import resources.database as database

def _is_embed(message):
    try:
        return message.embeds
    except Exception:
        return False


class Staff(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def take_order(payload, channel):
        message = await channel.fetch_message(payload.message_id)
        if (embed := _is_embed(message)):
            # TO DO
            # Get the existing 'GS-{order} worker' role and assign it to the staff member
            # Create a new channel in the 'in-progress' category so 'GS-{order}'
            # role can only read messages, the staff member can send messages
            # and management can manage all
            pass


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.client.get_channel(payload.channel_id)
        if payload.user_id != self.client.user.id:
            if channel.id == Channels.queued:
                # The reaction has been added in the 'queued' channel
                pass

            elif channel.category != None:
                if channel.category.id == Categories.in_progress:
                    # The reaction has been added in an order with 'in-progress' status
                    pass

                elif channel.category.id == Categories.pending_collection:
                    # The reaction has been added in an order with 'pending-collection' status
                    pass


def setup(client):
    client.add_cog(Staff(client))
