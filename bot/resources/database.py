import aiohttp
import asyncio
import json
from .constants import URL

__all__ = ['new_order', 'assign_order', 'set_progress', 'edit', 'collection', 'completed',
            'fetch_order', 'new_customer', 'check_customer', 'items', 'storages', 'status']

async def new_session():
    return aiohttp.ClientSession()

session = asyncio.get_event_loop().run_until_complete(new_session())

async def new_order(**kwargs):
    """Creates a new order in the database"""
    async with session.post(f'{URL}/orders/new', data=kwargs) as resp:
        return await resp.json()


async def assign_order(order: int, discord_id: int):
    """Assigns the given order to the worker"""
    async with session.patch(f'{URL}/orders/{order}/assign', data={'discord_id': discord_id}) as resp:
        return await resp.json()


async def set_progress(order: int, amount: int):
    """Changes the amount of an order"""
    async with session.patch(f'{URL}/orders/{order}/progress', data={'progress': amount}) as resp:
        return await resp.json()


async def edit(order: int, data: dict):
    """Edits the order details"""
    async with session.patch(f'{URL}/orders/{order}/edit', data=data) as resp:
        return await resp.json()


async def collection(order: int):
    """Puts the order in pending-collection status"""
    async with session.patch(f'{URL}/orders/{order}/collection') as resp:
        return await resp.json()


async def completed(order: int):
    """Changes the status of the order to completed"""
    async with session.patch(f'{URL}/orders/{order}/complete') as resp:
        return await resp.json()


async def cancel(order: int):
    """Cancels an order"""
    async with session.patch(f'{URL}/orders/{order}/cancel') as resp:
        return await resp.json()


async def fetch_order(order: int):
    """Returns an order data"""
    async with session.get(f'{URL}/orders/{order}') as resp:
        return await resp.json()


async def new_customer(data: dict):
    """Adds a new customer to the database"""
    async with session.post(f'{URL}/customers/new', data=data) as resp:
        return await resp.json()


async def check_customer(discord_id: int):
    """Checks if a customer exists"""
    async with session.get(f'{URL}/customers/{discord_id}') as resp:
        html = await resp.text()
        try:
            data = json.loads(html)
            return data
        except Exception:
            return False


async def fetch_items():
    """Returns all the items available"""
    async with session.get(f'{URL}/prices') as resp:
        html = await resp.json()
        items = {item['name'].lower(): [item['price'], item['limit']] for item in html}
        return items


async def fetch_storages():
    """Returns all the storages available"""
    async with session.get(f'{URL}.storages') as resp:
        html = await resp.json()
        storages = {storage['name'].lower(): [storage['id'], storage['fee']] for storage in html}
        return storages


async def status(discord_id):
    """Changes the status of the worker"""
    async with session.patch(f'{URL}/employees/{discord_id}/status') as resp:
        return await resp.json()['active']
