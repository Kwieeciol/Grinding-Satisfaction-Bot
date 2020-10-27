import discord
from discord.ext import commands
from resources.constants import MODERATION_ROLES, COLOUR, EMOJI_ID, Categories


def convert_args(args):
	available_options = ['amount', 'storage', 'discount', 'priority']

	if len(args) % 2 == 0:
		kwargs = {}
		for x in range(0, len(args), 2):
			kwargs[args[x].lower()] = args[x + 1]

		kwargs = {key: value for key, value in kwargs.items() if key in available_options}
		return kwargs

	else:
		return False


class Management(commands.Cog):
	def __init__(self, client):
		self.client = client


	@commands.command()
	@commands.has_role(MODERATION_ROLES)
	async def edit(self, ctx, *args):
		if (category := ctx.channel.category):
			if category.id == Categories.in_progress:
				if (options := convert_args(args)):
					for value in options.values():
						if not value.isdigit():
							await ctx.send(embed=discord.Embed(description=f'{emote} Please use only digits.', colour=COLOUR))
							break
				else:
					await ctx.send(embed=discord.Embed(description=f'{emote} Please use valid arguments **(priority, amount, storage, discount)**', colur=COLOUR))
			else:
				await ctx.send(embed=discord.Embed(description=f'{emote} Please use this command in a valid channel.', colour=COLOUR))
		else:
			await ctx.send(embed=discord.Embed(description=f'{emote} Please use this command in a valid channel.', colour=COLOUR))

def setup(client):
	client.add_cog(Management(client))