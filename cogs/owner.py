import discord
from discord.ext import commands, tasks

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx: commands.Context, *extensions):
        # Command for loading extensions
        for ext in extensions:
            try:
                self.bot.load_extension(f'cogs.{ext}')
            except Exception as e:
                return await ctx.send(f'Could not load `{ext}`')
        
        m = ', '.join(extensions)
        await ctx.send(f'Loaded `{m}`')
    
    
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, *extensions):
        # Command for reloading extensions
        for ext in extensions:
            try:
                self.bot.reload_extension(f'cogs.{ext}')
            except Exception as e:
                return await ctx.send(f'Could not reload `{ext}`')

        m = ', '.join(extensions)
        await ctx.send(f'Reloaded `{m}`')
    

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, *extensions):
        # Command for unloading extensions
        for ext in extensions:
            try:
                self.bot.unload_extension(f'cogs.{ext}')
            except Exception as e:
                return await ctx.send(f'Could not unload `{ext}`')
        
        m = ', '.join(extensions)
        await ctx.send(f'Unloaded `{m}`')
    

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx: commands.Context):
        # Command for shutting down the bot
        await ctx.send('Bot is shutting down')
        await self.bot.session.close()
        await self.bot.logout()
    

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def id(self, ctx: commands.Context):
        # Set of subcommands for getting the id of some object
        if ctx.invoked_subcommand is None:
            await ctx.send('Please use one of the following subcommands\n`member`, `channel`, `role`')


    @id.command()
    async def member(self, ctx: commands.Context, member: discord.Member):
        # Subcommand for getting the id of a member
        await ctx.send(f'{member.name}#{member.discriminator}: **{member.id}**')


    @id.command()
    async def channel(self, ctx: commands.Context, channel: discord.TextChannel):
        # Subcommand for getting the id of a channel
        await ctx.send(f'{channel.name}: **{channel.id}**')
    

    @id.command()
    async def role(self, ctx: commands.Context, role: discord.Role):
        # Subcommand for getting the id of a role
        await ctx.send(f'{role.name}: **{role.id}**')
    

def setup(bot):
    bot.add_cog(Owner(bot))