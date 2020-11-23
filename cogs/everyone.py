import time
import psutil
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
        # Stopping the embed
        end = time.perf_counter()
        total_time = (end - start) * 1000

        em.description = '```yaml\nLatency: {:.2f}ms\nPing:    {:.2f}ms```'.format(self.bot.latency * 1000, total_time)
        await message.edit(embed=em)


    @commands.command()
    async def stats(self, ctx):
        ram = dict(psutil.virtual_memory()._asdict())
        session_closed = str(self.bot.session.closed).lower()
        current_loop = self.bot.session_closed.current_loop
        total_ram = ram['total'] >> 20
        used_ram = ram['used'] >> 20

        content = f'```yaml\nSession closed: {session_closed}\nCurrent loop: {current_loop}\nUsed RAM: {used_ram}mb\nTotal RAM: {total_ram}mb```'
        embed = discord.Embed(title=f'Bot Statistics {self.bot.emoji}', description=content, colour=discord.Colour.greyple())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Everyone(bot))