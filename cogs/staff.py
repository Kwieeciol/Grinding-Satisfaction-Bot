import discord
from discord.ext import commands

class StaffCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_order_assign(self, ctx: commands.Context):
        order = await ctx.order
        print(order)
    

    @commands.Cog.listener()
    async def on_order_status_change(self, ctx: commands.Context):
        print(ctx)
    

    @commands.Cog.listener()
    async def on_order_complete(self, ctx: commands.Context):
        print(ctx)


    
def setup(bot):
    bot.add_cog(StaffCommands(bot))