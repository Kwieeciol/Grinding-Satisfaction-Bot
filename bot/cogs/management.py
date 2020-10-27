import discord
from discord.ext import commands
from resources.constants import MODERATION_ROLES, COLOUR


def check_keys(options):
	lst = [key.lower() in ['amount', 'storage', 'discount', 'priority'] for key in options.keys()]
	if False in lst:
		return False
	else:
		return True


def convert_args(args):
	if len(args) % 2 == 0:
		kwargs = {}
		for x in range(0, len(args), 2):
			kwargs[args[x]] = args[x + 1]

		return kwargs

	else:
		return False


class Management(commands.Cog):
	def __init__(self, client):
		self.client = client

	
	@commands.command()
	@commands.has_role(MODERATION_ROLES)
	async def edit(self, ctx, *args):
		if (options := convert_args(args)):
			if check_keys(options):
				pass
			else:
				pass



def setup(client):
	client.add_cog(Management(client))