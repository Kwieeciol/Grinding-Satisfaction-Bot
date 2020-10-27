import discord
from discord.ext import commands
import resources.database as database
from resources.functions import edit_embed
from resources.constants import MODERATION_ROLES, COLOUR, EMOJI_ID, Categories


def convert_args(args):
	available_options = ['amount', 'storage', 'discount', 'priority']
	print(args)

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

def setup(client):
	client.add_cog(Management(client))