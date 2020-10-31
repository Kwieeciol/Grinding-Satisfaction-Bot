import os
import yaml
import discord
from discord.ext import commands
from resources.constants import Channels, MODERATION_ROLES, STAFF_ROLES, COLOUR, EMOJI_ID


class Lottery(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.emote = f'<:gs:{EMOJI_ID}>'

    
    @commands.command(aliases=['nt'])
    @commands.has_role(MODERATION_ROLES)
    async def new_lottery(self, client, entries: int):
        def check(m):
            return not m.pinned

        data = {'lottery': {i: None for i in range(1, entries+1)}}

        channel = self.client.get_channel(Channels.lottery)
        content = '.\n'.join(str(i) for i in range(1, entries+1)) + '.'

        await channel.purge(limit=50, check=check)

        message = await channel.send(content)
        data['message_id'] = message.id

        with open('bot/resources/lottery.yaml', 'w') as file:
            yaml.dump(data, file)
    
    
    @commands.command(aliases=['l', 'lotto'])
    @commands.has_role(STAFF_ROLES)
    async def lottery(self, ctx, number: int):
        with open('bot/resources/lottery.yaml', 'r') as file:
            data = yaml.safe_load(file)
        
        count = len([entry for entry, value in data['lottery'].items() if value == ctx.author.id])

        if count < 3:
            if number in data['lottery']:
                if not data['lottery'][number]:
                    await ctx.send(embed=discord.Embed(description=f"{self.emote} You entered te lottery with **{number}**", colour=COLOUR))

                    data['lottery'][number] = ctx.author.id
                    with open('bot/resources/lottery.yaml', 'w') as file:
                        yaml.dump(data, file)

                    channel = self.client.get_channel(Channels.lottery)
                    message = await channel.fetch_message(data['message_id'])
                    
                    content = '\n'.join([f'{entry}. <@{user}>' if user != None else f'{entry}.' for entry, user in data['lottery'].items()])                    
                    await message.edit(content=content)
                else:
                    await ctx.send(embed=discord.Embed(description=f"{self.emote} Please choose another number.", colour=COLOUR))
            else:
                await ctx.send(embed=discord.Embed(description=f"{self.emote} Please choose a valid number.", colour=COLOUR))
        else:
            await ctx.send(embed=discord.Embed(description=f"{self.emote} You can't enter the lottery anymore.", colour=COLOUR))


def setup(client):
    client.add_cog(Lottery(client))