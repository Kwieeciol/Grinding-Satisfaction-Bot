import json
import discord
from discord.ext import commands
from bot import roles

def generate_lottery_message(data: dict):
    return '\n'.join([f'{num}.' if value is None else f'{num}. <@{value}>' for num, value in data.items()])


async def lottery_check(ctx: commands.Context, data: dict, choice: int) -> bool:
    content = data['lottery']

    entries = list(content.values()).count(ctx.author.id)

    if entries < 3:
        if choice in range(1, len(content) + 1):
            if data['lottery'][str(choice)] is None:
                return True
            else:
                await ctx.send("Please choose another number.")
        else:
            await ctx.send("Please choose another number.")
    else:
        await ctx.send("You can't enter the lottery anymore.")
    return False
        

class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['lotto', 'l'])
    @commands.has_role(roles['staff_role'])
    async def lottery(self, ctx: commands.Context, choice: int):
        with open('resources/lottery.json', 'r') as f:
            data = json.load(f)
        
        # Checking if the number is a valid choice
        is_valid_choice = await lottery_check(ctx, data, choice)

        if not is_valid_choice:
            return 

        lottery_channel = self.bot.channels['lottery']
        data['lottery'][str(choice)] = ctx.author.id

        with open('resources/lottery.json', 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"You entered the lottery with **{choice}**")
        # Fetching the message
        message = await lottery_channel.fetch_message(data['message_id'])
        # Generating the message
        message_content = await self.bot.loop.run_in_executor(None, generate_lottery_message, data['lottery'])
        # Editing the message
        await message.edit(content=message_content)
    
    
    @commands.command(aliases=['unlotto', 'unl'])
    @commands.has_role(roles['management_role'])
    async def unlottery(self, ctx: commands.Context, number: int):
        # Opening the file
        with open('resources/lottery.json', 'r') as f:
            data = json.load(f)
        
        lottery_channel = self.bot.channels['lottery']
        if number in range(1, len(data['lottery']) + 1):
            await ctx.send(f'Unlotted **{number}**')
            data['lottery'][str(number)] = None
            # Reseting the value in the file
            with open('resources/lottery.json', 'w') as f:
                json.dump(data, f, indent=4)
            # Fetching the message
            message = await lottery_channel.fetch_message(data['message_id'])
            # Generating the message
            message_content = await self.bot.loop.run_in_executor(None, generate_lottery_message, data['lottery'])
            # Editing the message
            await message.edit(content=message_content)
            
        else:
            await ctx.send("Please choose a valid number")


    @commands.command(aliases=['new_lotto', 'nl'])
    @commands.has_role(roles['management_role'])
    async def new_lottery(self, ctx: commands.Context, limit: int):
        lottery_channel = self.bot.channels['lottery']
        def check(m):
            return not m.pinned

        content_dict = {str(i): None for i in range(1, limit + 1)}
        # Generating the message
        content = await self.bot.loop.run_in_executor(None, generate_lottery_message, content_dict)

        await lottery_channel.purge(limit=50, check=check)
        message = await lottery_channel.send(content)

        data = {"message_id": message.id, "lottery": content_dict}
        # Dumping the data
        with open('resources/lottery.json', 'w') as f:
            json.dump(data, f, indent=4)


def setup(bot):
    bot.add_cog(Lottery(bot))