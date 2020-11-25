import os
import re
import json
import logging
from dotenv import load_dotenv
import asyncio
import aiohttp
import discord
from discord.ext import commands, tasks
from datetime import datetime
from utils.orders.database import database

__all__ = ['roles', 'GrindingSatisfactionBot']

initial_extensions = (
    'cogs.everyone',
    'cogs.owner',
    'cogs.customers',
    'cogs.staff',
    'cogs.lottery',
    'cogs.management'
)

roles = {
    'management_role': 741244092067086356,
    'staff_role': 713354499254648882
}

channels = {
    'lottery': 772182443800526858,
    'log': 771335478372204575,
    'orders': 740951313482907748
}

categories = {
    'pending_collection': 740923676115075132,
    'in_progress': 740923709568843848
}

def is_order_embed(message):
    title_pattern = '\*GS-\d+\*'
    author_pattern = '\w+#\d{4}'

    try:
        embed = message.embeds[0]

        title = embed.title
        author = embed.author.name
        fields = embed.fields

        if bool(re.search(title_pattern, title)):
            if bool(re.search(author_pattern, author)):
                if len(fields) in [5, 6]:
                    return True

        return False

    except Exception as e:
        return False


def return_int(s: str) -> int:
    return int(''.join(l for l in s if l.isdigit()))


class OrderContext(commands.Context):
    async def get_order(self):
        channel = self.channel

        if is_order_embed(self.message):
            if channel.id == channels['orders']:
                order_id = return_int(self.message.embeds[0].title)
                return await self.bot.database.fetch_order(order_id)
    
            if channel.category is not None:
                if channel.category.id in categories:
                    order_id = return_int(channel.name)
                    return await self.bot.database.fetch_order(order_id)

        return None


class GrindingSatisfactionBot(commands.Bot):
    def __init__(self, **options):
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(command_prefix='!', description='Grinding Satisfaction Bot for GSR', intents=intents,
                        case_insensitive=True)
        # Creating the session and db instance
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.database = database(self.session)

        self.format = options.pop('time_format', '[%H:%M:%S]')
        self.hide = options.pop('hide', True)

        self.channels = options.pop('channels', {})
        self.categories = options.pop('categories', {})
        # Setting up logging
        self.logging = options.pop('logging', True)

        if self.logging:
            logger = logging.getLogger('discord')
            logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
            handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
            logger.addHandler(handler)
        # Getting the process id
        self.pid = os.getpid()

        self.ignored_commands = options.pop('ignored_commands', [])
        # Loading extensions
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
                print('{0.time}\tLoaded extension {1}'.format(self, extension))
            except Exception as e:
                print('{0.time}\tFailed to load extension {1}'.format(self, extension))


    @property
    def time(self):
        return datetime.utcnow().strftime(self.format)
    
    
    @tasks.loop(seconds=60.0)
    async def session_closed(self):
        # Creates a new session whenever the old one is closed
        if self.session.closed:
            print('{0.time}\tSession is closed... Creating a new one'.format(self))
            self.session = aiohttp.ClientSession(loop=self.loop)
            print('{0.time}\tSuccesfully created a new session'.format(self))


    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.utcnow().strftime(self.format)

        await self.wait_until_ready()
        # Getting the owner `me` and the GS emoji
        self.owner = await self.fetch_user(675002733056622592)
        self.emoji = self.get_emoji(745358651967012994)
        # Getting the channels
        for name, id in channels.items():
            obj = self.get_channel(id)
            self.channels[name] = obj
        # Getting the categories
        for name, id in categories.items():
            obj = self.get_channel(id)
            self.categories[name] = obj

        print('{0.uptime}\t{0.user} has logged in'.format(self))
        self.session_closed.start()
        print('{0.time}\tTask started'.format(self))
    

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or OrderContext)


    async def on_command(self, ctx):
        command = str(ctx.command).lower()
        if command in self.ignored_commands:
            return

        print('{0.time}\t`{1.command}` used by `{1.author}`'.format(self, ctx))


    async def on_command_error(self, ctx, error):
        # Global error handler
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command does not exist')
        else:
            print(error)
    

    async def on_message(self, message):
        if message.author == self.user:
            return

        if not self.hide:
            print('{0.time}\t{1.id} sent by {1.author} in {1.channel}'.format(self, message))

        await self.process_commands(message) 
    

    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.user.id:
            return
        
        if not self.hide:
            member = await self.fetch_user(payload.user_id)
            print('{0.time}\t{1.emoji} added on {1.message_id} by {2}'.format(self, payload, member))

        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if str(payload.emoji) == '✅':
            if is_order_embed(message):
                # Getting the context, worker and order objects
                context = await self.get_context(message)
                worker = channel.guild.get_member(payload.user_id)
                # order = await self.database.get_order(return_int(channel.name))
                # Dispaching custom events
                if channel == self.channels['orders']:
                    self.dispatch('order_assign', context, worker, order)
                
                elif channel.category == self.categories['in_progress']:
                    self.dispatch('order_status_change', context, worker, order)
                
                elif channel.category == self.categories['pending_collection']:
                    self.dispatch('order_complete', context, worker, order)
    

    async def on_connect(self):
        print('{0.time}\t{0.user} has connected'.format(self))
    

    async def on_resumed(self):
        print('{0.time}\t{0.user} has resumed'.format(self))
    

    async def on_disconnected(self):
        print('{0.time}\t{0.user} has disconnected'.format(self))
        await self.session.close()
    

    def get_token(self, path='.env'):
        load_dotenv()
        return os.getenv('TOKEN')

    
    def run(self):
        print('{0.time}\tRunning...'.format(self))
        TOKEN = self.get_token()
        super().run(TOKEN)
