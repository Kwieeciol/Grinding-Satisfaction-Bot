from dateutil import parser

def convert_time(string: str) -> str or None:
    try:
        return parser.parse(string)
    except Exception as e:
        return None


class Customer:
    def __init__(self, session, **data):
        self._data = data
        self.session = session
        self.id = data['id']
        self.name = data['name']
        self.discord_id = data['discord_id']
        self.tycoon_name = data['tycoon_name']
        self.tycoon_id = data['tycoon_id']
    

    def __eq__(self, other):
        return self._data == other._data
    

    def __ne__(self, other):
        return self._data != other._data

    
    def __gt__(self, other):
        return self.id > other.id
    

    def __lt__(self, other):
        return self.id < other.id


class Employee:
    def __init__(self, session, **data):
        self._data = data
        self.session = session
        self.id = data['id']
        self.name = data['name']
        self.discord_id = data['discord_id']
        self.url = f'http://grindingsatisfaction.herokuapp.com/employees/{self.discord_id}'
        self.rank = data['rank']
        self.trainee = data['trainee']
        self.joined_at = convert_time(data['joined_at'])
        self.active = data['active']
        self.trailer = data['trailer']
        self.faction = data['faction']
        self.management = data['management']
    

    async def promote(self):
        """|coro|
        
        Promotes am employee
        
        """
        async with self.session.patch(f'{self.url}/promote') as resp:
            data = await resp.json()
            self._update(**data)
    

    async def trainee(self):
        """|coro|
        
        Sets the trainee to True or False accordingly

        """
        async with self.session.patch(f'{self.url}/trainee') as resp:
            data = await resp.json()
            self._update(**data)
    

    async def status(self):
        """|coro|

        Changes the status of the employee to `active` or `inactive`
        
        """
        async with self.session.patch(f'{self.url}/status') as resp:
            data = await resp.json()
            self._update(**data)
    

    async def trailer(self, trailer: int):
        """|coro|

        Changes the trailer of the employee
        
        """
        async with self.session.patch(f'{self.url}/trailer', data={'trailer': trailer}) as resp:
            data = await resp.json()
            self._update(**data)
    

    async def faction(self, faction: str):
        """|coro|
        
        Changes the faction of the employee

        """
        async with self.session.patch(f'{self.url}/faction', data={'faction': faction}) as resp:
            data = await resp.json()
            self._update(**data)


    def _update(self, **data):
        """Updates the attributes"""
        for key, value in data.items():
            setattr(self, key, value)
    

    def __eq__(self, other):
        return self._data == other._data
    

    def __ne__(self, other):
        return self._data != other._data

    
    def __gt__(self, other):
        return self.id > other.id
    

    def __lt__(self, other):
        return self.id < other.id


class Storage:
    def __init__(self, session, **data):
        self._data = data
        self.session = session
        self.id = data['id']
        self.name = data['name']
        self.fee = data['fee']
        self.faction = data['faction']
    

    def __eq__(self, other):
        return self._data == other._data
    

    def __ne__(self, other):
        return self._data != other._data

    
    def __gt__(self, other):
        return self.id > other.id
    

    def __lt__(self, other):
        return self.id < other.id


class Item:
    def __init__(self, session, **data):
        self._data = data
        self.session = session
        self.id = data['id']
        self.created_at = convert_time(data['created_at'])
        self.updated_at = convert_time(data['updated_at'])
        self.name = data['name']
        self.price = data['price']
        self.limit = data['limit']
    

    def __eq__(self, other):
        return self._data == other._data
    

    def __ne__(self, other):
        return self._data != other._data

    
    def __gt__(self, other):
        return self.id > other.id
    

    def __lt__(self, other):
        return self.id < other.id


class Order:
    def __init__(self, session, **data):
        self._data = data
        self.session = session
        self.id = data['id']
        self.url = f'http://grindingsatisfaction.herokuapp.com/orders/{self.id}'
        self.created_at = convert_time(data['created_at'])
        self.updated_at = convert_time(data['updated_at'])
        self.priority = data['priority']
        self.status = data['status']
        self.progress = data['progress']
        self.customer = Customer(**data['customer'])
        self.item = Item(**data['product_name'])
        self.amount = data['amount']
        self.discount = data['discount']
        self.storage = Storage(**data['storage'])
        self.assigned_at = convert_time(data['assigned_at'])
        self.fulfilled_at = convert_time(data['fulfilled_at'])
        self.completed_at = convert_time(data['completed_at'])
        self.total_price = data['total_price']
        try:
            self.worker = Employee(**data['worker_id'])
        except Exception as e:
            self.worker = None

    
    async def assign(self, employee):
        """|coro|
        
        Assigns an order to the employee

        Parameters
        ----------
        employee :class: `~abc.Employee`
        """
        async with self.session.patch(f'{self.url}/assign', data={'discord_id': employee.discord_id}) as resp:
            data = await resp.json()
            self._update(**data)

    
    async def unassign(self):
        """|coro|
        
        Unassigns an order
        
        """
        async with self.session.patch(f'{self.url}/unassign') as resp:
            data = await resp.json()
            self._update(**data)

    
    async def progress(self, amount: int):
        """|coro|
        
        Sets the progress to the given amount

        Parameters
        ----------
        amount :class: `~int`
            The amount which to set
        """
        async with self.session.patch(f'{self.url}/progress', data={'progress': amount}) as resp:
            data = await resp.json()
            self._update(**data)

    
    async def collection(self):
        """|coro|
        
        Sets the order to `pending-collection` status
        
        """
        async with self.session.patch(f'{self.url}/collection') as resp:
            data = await resp.json()
            self._update(**data)


    async def complete(self):
        """|coro|
        
        Sets the order to `completed` status
        
        """
        async with self.session.patch(f'{self.url}/complete') as resp:
            data = await resp.json()
            self._update(**data)
        

    async def edit(self, **options):
        """|coro|

        Edits an order

        Parameters
        ----------
        \*\*options
            Keyword arguments that should be changed
        """
        async with self.session.patch(f'{self.url}/edit', data=options) as resp:
            data = await resp.json()
            self._update(**data)
    

    async def cancel(self):
        """|coro|
        
        Cancels an order
        
        """
        async with self.session.patch(f'{self.url}/cancel') as resp:
            data = await resp.json()
            self._update(**data)


    def _update(self, **data):
        """Updates the attributes"""
        for key, value in data.items():
            setattr(self, key, value)


    def __eq__(self, other):
        return self._data == other._data
    

    def __ne__(self, other):
        return self._data != other._data
    

    def __gt__(self, other):
        return self.id > other.id
    

    def __lt__(self, other):
        return self.id < other.id