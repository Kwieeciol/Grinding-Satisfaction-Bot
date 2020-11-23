import asyncio
import abc

class database:
    def __init__(self, session):
        self.url = 'http://grindingsatisfaction.herokuapp.com'
        self.session = session

    async def fetch_order(self, order_id: int):
        """|coro|

        Retrievies a single order from the database

        Parameters
        ----------
        order_id :class:`int`
            The order ID to look for.

        
        Returns
        ----------
        :class:`~abc.Order`
        """
        async with self.session.get(f'{self.url}/orders/{order}') as resp:
            data = await resp.json()
            return abc.Order(self.session **data)
    

    async def fetch_orders(self):
        """|coro|

        Retrievies all orders from the database
        
        Returns
        ----------
        List[:class:`~abc.Order`]
            All of the orders in the database.
        """
        async with self.session.get(f'{self.url}/orders') as resp:
            data = await resp.json()
            output = []
            for order in data:
                output.append(abc.Order(self.session, **order))
            return output
    

    async def new_order(self, **kwargs):
        """|coro|

        Creates a new order

        Parameters
        ----------
        \*\*kwargs
            New order details

        Returns
        ----------
        :class: `~abc.Order`
        """
        async with self.session.post(f'{self.url}/orders/new', data=kwargs) as resp:
            data = await resp.json()
            return abc.Order(self.session, **data)


    async def fetch_customer(self, discord_id: int):
        """|coro|

        Retrievies a single customer from the database

        Parameters
        ----------
        discord_id: :class:`int`
            The discord ID of the customer to look for.

        
        Returns
        ----------
        :class:`~abc.Customer`
        """
        async with self.session.get(f'{self.url}/customers/{discord_id}') as resp:
            data = await resp.json()
            return abc.Customer(self.session, **data)


    async def fetch_customers(self):
        """|coro|

        Retrievies all customers from the database
        
        Returns
        ----------
        :class:`~abc.Customer`
        """
        async with self.session.get(f'{self.url}/customers') as resp:
            data = await resp.json()
            output = []
            for customer in data:
                output.append(abc.Customer(self.session, **customer))
            return output

    
    async def new_customer(self, **kwargs):
        """|coro|
        
        Creates a new customer

        Parameters
        ----------
        \*\*kwargs
            Customer details
        
        Returns
        ----------
        :class:`~abc.Customer`
        """
        async with self.session.post(f'{self.url}/customers/new', data=kwargs) as resp:
            data = await resp.json()
            return abc.Customer(self.session, **data)


    async def fetch_employee(self, discord_id: int):
        """|coro|

        Retrievies an employee from the database

        Parameters
        ----------
        discord_id: :class:`int`
            The employee ID to look for.

        
        Returns
        ----------
        :class:`~abc.Employee`
        """
        async with self.session.get(f'{self.url}/employees/{discord_id}') as resp:
            data = await resp.json()
            return abc.Employee(self.session, **data)
    

    async def fetch_employees(self):
        """|coro|

        Retrievies all employees from the database
        
        Returns
        ----------
        :class:`~abc.Employee`
        """
        async with self.session.get(f'{self.url}/employees') as resp:
            data = await resp.json()
            output = []
            for employee in data:
                output.append(abc.Employee(self.session, **employee))
            return output

    
    async def new_employee(self, **kwargs):
        """|coro|
        
        Creates a new employee

        Parameters
        ----------
        \*\*kwargs
            Employee data

        Returns
        ----------
        :class:`~abc.Employee`
        """
        async with self.session.post(f'{self.url}/employees/new', data=kwargs) as resp:
            data = await resp.json()
            return abc.Employee(self.session, **data)


    async def fetch_storage(self, storage_id: int):
        """|coro|

        Retrievies a single storage from the database

        Parameters
        ----------
        storage_id: :class:`int`
            The storage ID to look for.

        
        Returns
        ----------
        :class:`~abc.Storage`
        """
        async with self.session.get(f'{self.url}/storages/{storage}') as resp:
            data = await resp.json()
            return abc.Storage(self.session, **data)
    

    async def fetch_storages(self):
        """|coro|

        Retrievies all storages from the database

        Returns
        ----------
        List[:class:`~abc.Storage`]
        """
        async with self.session.get(f'{self.url}/storages') as resp:
            data = await resp.json()
            output = []
            for storage in data:
                output.append(abc.Storage(self.session, **storage))
            return output


    async def fetch_item(self, item_id: int):
        """|coro|

        Retrievies a single item from the database

        Parameters
        ----------
        item_id: :class:`int`
            The storage ID to look for.

        
        Returns
        ----------
        :class:`~abc.Item`
        """
        async with self.session.get(f'{self.url}/prices/{item_id}') as resp:
            data = await resp.json()
            return abc.Item(self.session, **data)
    

    async def fetch_items(self):
        """|coro|

        Retrievies all items from the database

        Returns
        ----------
        List[:class:`~abc.Item`]
        """
        async with self.session.get(f'{self.url}/prices') as resp:
            data = await resp.json()
            output = []
            for item in data:
                output.append(abc.Item(self.session, **item))
            return output

