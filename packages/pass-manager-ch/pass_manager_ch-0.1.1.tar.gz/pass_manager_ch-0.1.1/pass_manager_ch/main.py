import json
import click
from rocksdict import Rdict
from hashlib import sha256
from secrets import token_urlsafe
from urllib.parse import quote
from dataclasses import dataclass, asdict, is_dataclass
from rocksdict import Rdict

class MetaDataObject(type):
	def __new__(mcs,name:str,bases:tuple[type],namespace:dict[str,object]):
		klass = super().__new__(mcs,name,bases,namespace)
		if is_dataclass(klass):
			return klass
		return dataclass(klass)
	

@dataclass
class BaseModel(metaclass=MetaDataObject):
	def json(self):
		return json.dumps(self.dict())
	def dict(self):
		return asdict(self)
	def __hash__(self):
		return int(sha256(self.json().encode()).hexdigest(),16)
	@classmethod
	def db(cls):
		return Rdict(cls.__name__.lower())
	
@dataclass
class PasswordEntry(BaseModel):
    id: str
    url: str
    password: str

    @staticmethod
    def generate_password(length: int = 16):
        return token_urlsafe(length)[:length]

    def save(self):
        db = self.db()
        db[self.id] = self.dict()

    @classmethod
    def get(cls, entry_id: str):
        db = cls.db()
        data = db.get(entry_id)
        if data:
            return cls(**json.loads(data))
        return None

    @classmethod
    def delete(cls, entry_id: str):
        db = cls.db()
        if entry_id in db:
            del db[entry_id]

    @classmethod
    def find(cls, url: str = None):
        db = cls.db()
        results = []
        for key, value in db.iter():
            entry = json.loads(value)
            if url is None or entry['url'] == url:
                results.append(cls(**entry))
        return results


@click.group()
def cli():
    """Password Manager CLI"""
    pass


@cli.command()
@click.option('--url', default=None, help='The URL to search for. Leave empty to list all entries.')
def find(url):
    """Find password entries by URL or list all entries"""
    entries = PasswordEntry.find(url)
    if entries:
        for entry in entries:
            click.echo(f"Found entry with ID {entry.id} - URL: {entry.url} - Password: {entry.password}")
    else:
        click.echo("No entries found.")


@cli.command()
@click.option('--url', prompt=True, help='The URL for the password entry.')
@click.option('--password', default=None, help='The password. If not provided, a random one will be generated.')
def add(url, password):
    """Add a new password entry"""
    entry_id = sha256(url.encode()).hexdigest()
    password = password or PasswordEntry.generate_password()
    entry = PasswordEntry(id=entry_id, url=url, password=password)
    entry.save()
    click.echo(f"Password entry added for {url} with ID {entry_id}.")


@cli.command()
@click.option('--entry-id', prompt=True, help='The ID of the password entry to retrieve.')
def get(entry_id):
    """Get a password entry by ID"""
    entry = PasswordEntry.get(entry_id)
    if entry:
        click.echo(f"URL: {entry.url}\nPassword: {entry.password}")
    else:
        click.echo(f"No entry found with ID {entry_id}.")


@cli.command()
@click.option('--entry-id', prompt=True, help='The ID of the password entry to delete.')
def delete(entry_id):
    """Delete a password entry by ID"""
    entry = PasswordEntry.get(entry_id)
    if entry:
        PasswordEntry.delete(entry_id)
        click.echo(f"Deleted entry with ID {entry_id}.")
    else:
        click.echo(f"No entry found with ID {entry_id}.")
    cli()