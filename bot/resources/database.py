import aiohttp
import asyncio
import json
from .constants import URL

__all__ = ['session', 'new_order', 'assign_order', 'set_progress', 'edit', 'collection', 'completed',
            'fetch_order', 'new_customer', 'check_customer', 'items', 'storages', 'status']

async def new_session():
    return aiohttp.ClientSession()

session = asyncio.get_event_loop().run_until_complete(new_session())

async def new_order(data: dict):
    """Creates a new order in the database.

    Returns:
        [dict]: Order data
    """
    async with session.post(f'{URL}/orders/new', data=data) as resp:
        return await resp.json()


async def assign_order(order: int, discord_id: int):
    """Assigns the given order to the worker

    Args:
        order (int): The order ID
        discord_id (int): Discord ID of the worker which to assign the order

    Returns:
        [dict]: Order data
    """
    async with session.patch(f'{URL}/orders/{order}/assign', data={'discord_id': discord_id}) as resp:
        return await resp.json()


async def set_progress(order: int, amount: int):
    """Changes the amount of an order

    Args:
        order (int): The order ID
        amount (int): Amount to to update in the database

    Returns:
        [dict]: Order data
    """
    async with session.patch(f'{URL}/orders/{order}/progress', data={'progress': amount}) as resp:
        return await resp.json()


async def edit(order: int, data: dict):
    """Edits the order details

    Args:
        order (int): The order ID
        data (dict): Dictionary with details to change

    Returns:
        [dict]: Order data
    """
    async with session.patch(f'{URL}/orders/{order}/edit', data=data) as resp:
        return await resp.json()


async def collection(order: int):
    """Changes the order status to 'pending-collection'

    Args:
        order (int): The order ID

    Returns:
        [dict]: Order data
    """
    async with session.patch(f'{URL}/orders/{order}/collection') as resp:
        return await resp.json()


async def completed(order: int):
    """Changes the order status to 'completed'

    Args:
        order (int): The order ID

    Returns:
        [dict]: Order data
    """
    async with session.patch(f'{URL}/orders/{order}/complete') as resp:
        return await resp.json()


async def cancel(order: int):
    """Cancel an order

    Args:
        order (int): The order ID

    Returns:
        [dict]: Order data
    """
    async with session.patch(f'{URL}/orders/{order}/cancel') as resp:
        return await resp.json()


async def fetch_order(order: int):
    """Returns an order data

    Args:
        order (int): The order ID

    Returns:
        [dict]: Order data
    """
    async with session.get(f'{URL}/orders/{order}') as resp:
        return await resp.json()


async def new_customer(data: dict):
    """Adds a new customer to the database

    Args:
        data (dict): Customer details

    Returns:
        [dict]: Customer data
    """
    async with session.post(f'{URL}/customers/new', data=data) as resp:
        return await resp.json()


async def check_customer(discord_id: int):
    """Checks if a customer exists

    Args:
        discord_id (int): The discord ID

    Returns:
        [dict/NoneType]: Customer data
    """
    async with session.get(f'{URL}/customers/{discord_id}') as resp:
        html = await resp.text()
        try:
            data = json.loads(html)
            return data
        except Exception:
            return None


async def fetch_items():
    """Returns all available items

    Returns:
        [dict]: Items details
    """
    async with session.get(f'{URL}/prices') as resp:
        html = await resp.json()
        items = {item['name'].lower(): {'id': item['id'], 'price': item['price'], 'limit': item['limit']} for item in html}
        return items


async def fetch_storages():
    """Returns all available storages

    Returns:
        [dict]: Storages details
    """
    async with session.get(f'{URL}/storages') as resp:
        html = await resp.json()
        storages = {storage['name'].lower(): {'id': storage['id'], 'fee': storage['fee']} for storage in html}
        return storages


async def status(discord_id: int):
    """Switches the worker status between active/inactive

    Args:
        discord_id (int): The worker discord ID

    Returns:
        [bool]: Active/inactive
    """
    async with session.patch(f'{URL}/employees/{discord_id}/status') as resp:
        return await resp.json()['active']
