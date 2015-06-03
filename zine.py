#!/usr/bin/env python
import datetime
import re
import sys

from blessings import Terminal
from peewee import *

t = Terminal()
MESSAGES = []
DATABASE = SqliteDatabase('zines.db')

#helpful functions

def title_order(string):
    """Return a string with funny and unhelpful characters removed from the front"""
    title_portion = re.compile(r"[A-Za-z0-9].+")
    try:
        return title_portion.search(string).group().lower()
    except:
        return string.lower()


def get_format():
    """Prompt user for format of zine"""
    FORMATS = ['HALF-SIZE', 'FULL-SIZE', 'QUARTER-SIZE', 'HALF-LEGAL', 'ODD-SIZE', 'BOOK', 'MAGAZINE']

    for index, _format in enumerate(FORMATS):
        print "({}) {}".format(index + 1, _format)
    try:
        f = int(raw_input("Which format? > ").strip())
        return FORMATS[f-1]
    except:
        get_format()

def get_genre():
    """Prompt user for genre of zine"""
    GENRES = ['PERZINE', 'FANZINE', 'LITZINE', 'HUMOUR', 'CULTURE', 'MISCELLANEOUS', 'GENDER/QUEER', 'POLITICS']
    for index, _format in enumerate(GENRES):
        print "({}) {}".format(index + 1, _format)
    try:
        f = int(raw_input("Which genre? > ").strip())
        return GENRES[f-1]
    except:
        get_genre()

def get_title():
    """Prompt user for title"""
    title = raw_input("Enter title > ").strip()
    confirm = raw_input('Confirm "{}" [yN] > '.format(title)).lower()
    if confirm == 'y':
        return title
    else:
        get_title()

def get_author():
    """Prompt user for author"""
    author = raw_input("Enter author > ").strip()
    confirm = raw_input('Confirm "{}" [yN] > '.format(author)).lower()
    if confirm == 'y':
        return author
    else:
        get_author()

def add_zine():
    title = get_title()
    author = get_author()
    genre = get_genre()
    zine_format = get_format()
    try:
        Zine.new(title = title, author = author, genre = genre, zine_format = zine_format)
        MESSAGES.append("{} added!".format(title))
        main_menu()
    except Exception as inst:
        print inst
        main_menu()


#def get_spacings(result_set):
    #"""get the maximum length for each field in result"""
    #pass

#def format_line(result, spacing):
    #"""return a line with correct spacing and padding"""
    #pass


def search_zines():
    query = raw_input("Enter search string > ")
    query = '%' + query + '%'
    results = Zine.select().where( (Zine.title ** query) | (Zine.author ** query)).order_by( Zine.title_order )
    if results.count() == 0:
        print "No results!"
    else:
        #id_space, title_space, author_space, genre_space, format_space = get_spacings(results)   
        for result in results:
            MESSAGES.append("{} {} {} {} {}".format(result.id, result.title, result.author, result.genre, result.zine_format))
            MESSAGES.append("{} {} {} {} {}".format("-"*len(str(result.id)), "-"*len(result.title), "-"*len(result.author), "-"*len(result.genre), "-"*len(result.zine_format)))

    main_menu()    

def edit_zine():
    try:
        zine_id = int(raw_input("Enter ID of zine to search > "))
    except:
        print "Please enter a valid number!"
    else:
        results = Zine.select().where(Zine.id == zine_id)
        if results.count() == 0:
            print "No zine with that ID"
        else:
            result = results.first()
            print "Found {} {} {} {}".format(result.title, result.author, result.genre, result.zine_format)
            values = {'title': result.title, 'author':result.author, 'genre':result.genre, 'format':result.zine_format}
            new_title = raw_input("Enter new title? [yN] > ")
            if new_title.lower() == 'y':
                values['title'] = get_title()
            new_author = raw_input("Enter new author? [yN] > ")
            if new_author.lower() == 'y':
                values['author'] = get_author()
            new_genre = raw_input("Enter new genre? [yN] > ")
            if new_genre.lower() == 'y':
                values['genre'] = get_genre()
            new_format = raw_input("Enter new format? [yN] > ")
            if new_format.lower() == 'y':
                values['format'] = get_format()
            print "New record: {}".format(values)
            accept = raw_input("Accept? [yN] > ")
            if accept.lower() == 'y':
                print "Updating database!"
                q = Zine.update(title = values['title'], author = values['author'], zine_format = values['format'], genre = values['genre']).where(Zine.id == zine_id)
                q.execute()

    main_menu()

def main_menu():
    OPTIONS = ['ADD ZINE', 'SEARCH ZINES', 'EDIT ZINE', 'QUIT']
    with t.fullscreen():
        print "#"*40
        print "#"  + (" "* 38) + "#"
        print "#"  + (" " * 13) + "TORONTO" + (" " * 18) + "#"
        print "#"  + (" " * 13) + "ZINE" + (" " * 21) + "#"
        print "#"  + (" " * 13) + "LIBRARY" + (" " * 18) + "#"
        print "#"  + (" " * 38) + "#"
        print "#"*40
        if len(MESSAGES) > 0:
            while len(MESSAGES) > 0:
                m = MESSAGES.pop()
                print m
            print "\n"    
        for index, option in enumerate(OPTIONS):
            print t.bold("({}) {}".format(index + 1, option))
        try:
            f = int(raw_input("Enter choice > ").strip())
        except:
            main_menu()
        if f in range(1, len(OPTIONS) + 1):    
            if OPTIONS[f-1] == 'ADD ZINE':
                add_zine()
            elif OPTIONS[f-1] == 'SEARCH ZINES':
                search_zines()
            elif OPTIONS[f-1] == 'EDIT ZINE':
                edit_zine()    
            elif OPTIONS[f-1] == 'QUIT':
                print "Goodbye!"
                exit(0)
        else:
            main_menu()                
          

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
    
    @classmethod
    def new(cls, title, author, genre, zine_format, description = None):
        cls.create(title = title, title_order = title_order(title), author = author, genre = genre, zine_format = zine_format, description = description)
   
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
   
       

def initialize():
    DATABASE.create_tables([Zine, Patron, Borrowed])
    DATABASE.close()

if __name__ == '__main__':
    try:
        initialize()
    except:
        pass    
    main_menu()
