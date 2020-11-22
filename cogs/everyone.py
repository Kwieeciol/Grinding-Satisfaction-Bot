import time
import discord
from discord.ext import commands


class Everyone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        # Starting the counter
        start = time.perf_counter()
        em = discord.Embed(title=f'Pong! {self.bot.emoji}', colour=discord.Colour.greyple())
        message = await ctx.send(embed=em)
        # Stopping the timer
        end = time.perf_counter()
        total_time = (end - start) * 1000

        em.description = '```yaml\nLatency: {:.2f}ms\nPing:    {:.2f}ms```'.format(self.bot.latency * 1000, total_time)
        await message.edit(embed=em)


def setup(bot):
    bot.add_cog(Everyone(bot))
