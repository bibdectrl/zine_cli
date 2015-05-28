import datetime
import re

from peewee import *


DATABASE = SqliteDatabase('zines.db')

FORMATS = ['HALF-SIZE', 'FULL-SIZE', 'QUARTER-SIZE', 'HALF-LEGAL', 'ODD-SIZE', 'BOOK', 'MAGAZINE']

GENRES = ['PERZINE', 'FANZINE', 'LITZINE', 'HUMOUR', 'MISCELLANEOUS', 'GENDER/QUEER', 'POLITICS']


#helpful functions

def title_order(string):
    title_portion = re.compile(r"[A-Za-z0-9].+")
    try:
        return title_portion.search(string).group()
    except:
        return string

def edit_distance(s1, s2):
    pass


class BaseModel(Model):
    class Meta:
        database = DATABASE

class Zine(BaseModel):
    title = CharField()
    date_added = DateTimeField(default = datetime.datetime.now)
    title_order = CharField()
    author = CharField()
    genre = CharField()
    description = CharField(null = True)
    zine_format = CharField()
    
    class Meta:
        order_by = ('title_order',)


class Patron(BaseModel):
    name = CharField()
    contact = CharField()


class Borrowed(BaseModel):
    patron = ForeignKeyField(Patron, related_name = 'patron')
    zine = ForeignKeyField(Zine, related_name = 'zine')
    borrowed_on = DateTimeField()
    due_date = DateTimeField()
   
    @classmethod
    def new(cls, title, author, genre, zine_format, description = None):
        cls.create( title = title, title_order = title_order(title), author = author, genre = genre, zine_format = zine_format, description = description)
       

def initialize():
    DATABASE.create_tables([Zine, Patron, Borrowed])
    DATABASE.close()

if __name__ == '__main__':
    initialize()
    
    
