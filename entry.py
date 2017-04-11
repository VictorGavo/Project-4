from collections import OrderedDict
import datetime
from datetime import date
import os
import sys
import pdb

from peewee import *

db = SqliteDatabase('worklog.db')


class Entry(Model):
    name = CharField(max_length=255)
    task = CharField(max_length=255)
    duration = IntegerField()
    notes = TextField()
    timestamp = DateField(default=datetime.date.today)

    class Meta:
        database = db


def clear():
    """Clear the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


def menu_loop(test=False):
    """Show the menu."""
    choice = None
    while choice != 'q':
        print("Enter 'q' to quit.")
        print("[1] Add an entry.")
        print("[2] Look up entries.")
        if test == False:
            choice = inputter('menu', input("> "))
        else:
            choice = test

        if choice == '1':
            name = inputter('name', input("Name: "))
            task = inputter('task', input("Task: "))
            duration = inputter('duration', input("Duration (in minutes): "))
            notes = inputter('notes', input("Notes: "))
            add_entry(name, task, duration, notes)
        elif choice == '2':
            menu_lookup(test=test)
        else:
            print("I'm afraid I can't let you do that Dave.")
        if test != False:
            choice = 'q'
    return choice


def menu_lookup(test=False, query=False):
    """Lookup entries."""
    choice = None

    while choice != 'q':
        print("Enter 'q' to return to the previous menu.")
        print("[1] Find all entries from an employee.")
        print("[2] Find all entries pertaining to a term.")
        print("[3] Find all entries based on time spent.")
        print("[4] Lookup entries by date.")
        if test == False:
            choice = inputter('menu', input("> "))
        else:
            choice = test

        if choice == '1':
            query = inputter('query', input("Enter a name: ")).capitalize()
            menu_list('employee', query)
        elif choice == '2':
            query = inputter('query', input("Enter a term: "))
            menu_list('term', query)
        elif choice == '3':
            query = inputter('duration', input("Enter a number of minutes: "))
            menu_list('duration', query)
        elif choice == '4':
            menu_date(test=test)
        else:
            print("I'm afraid I can't let you do that Dave.")
        if test != False:
            choice = 'q'

    return choice


def menu_date(test=False):
    """Lookup entries by date."""
    choice = None

    while choice != 'q':
        print("Enter 'q' to return to the previous menu.")
        print("[1] Find all entries in a range of dates.")
        print("[2] List all entries by date.")
        if test == False:
            choice = inputter('menu', input("> "))
        else:
            choice = test

        if choice == '1':
            try:
                query = [inputter('date', input("Enter the first date: ")),
                        inputter('date', input("Enter the second date: "))]
                menu_list('range', query, test=test)
            except TypeError:
                pass
        elif choice == '2':
            menu_list('all', query=None)
        else:
            print("I'm afraid I can't let you do that Dave.")
        if test != False:
            choice = 'q'
    return choice


def menu_list(search_by, query, test=False):
    choice = None
    while choice != 'q':
        entries = get_entries(search_by, query)
        if entries:
            print("Enter 'q' to return to the previous menu.")
            count = 0
            for entry in entries:
                count += 1
                print("[{}] {}, {}".format(count, entry.name, entry.task))
            if test == False:
                choice = inputter('entry', input("Select an entry: "))
            else:
                choice = test
            if choice == 'q':
                break
            elif int(choice) > len(entries) or int(choice) <= 0:
                print("That is not an option")
            else:
                choice = int(choice) - 1
                menu_entry(entries, choice, test=test)
        elif search_by == None:
            pass
        else:
            clear()
            print("No entries were found that match your search criteria.")
            break
        if test != False:
            choice = 'q'
    return str(choice)


def get_entries(search_by, query):
    if search_by == 'all':
        return Entry.select()
    elif search_by == 'employee':
        return find_by_employee(query)
    elif search_by == 'term':
        return find_by_term(query)
    elif search_by == 'duration':
        return find_by_duration(query)
    elif search_by == 'range':
        return find_by_range(query[0], query[1])


def menu_entry(entries, choice, test=False):
    index = choice
    choice = None
    while choice != 'q':
        print("Enter 'q' to return to the previous menu.")
        display(entries[index])
        print("\n")
        try:
            entries[index+1]
            print("[n] next entry")
        except IndexError:
            pass
        try:
            entries[index-1]
            print("[p] previous entry")
        except ValueError:
            pass
        print("[e] edit entry")
        print("[d] delete entry")
        if test == False:
            choice = inputter('menu', input("> "))
        else:
            choice = test
        clear()

        if choice == 'e':
            menu_edit(entries[index], test=test)
        elif choice == 'd':
            if inputter('delete', input("Are you sure? (yN): ")).lower() == 'y':
                delete_entry(entries[index])
            else:
                pass
        elif choice == 'p':
            try:
                entries[index-1]
                clear()
                index -= 1
                menu_entry(entries, index, test=test)
            except ValueError:
                clear()
                print("This is the first entry.")
                # menu_entry(entries, index)
        elif choice == 'n':
            try:
                entries[index+1]
                clear()
                index += 1
                menu_entry(entries, index, test=test)
            except IndexError:
                clear()
                print("This is the last entry.")
                # menu_entry(entries, index)
        else:
            print("Not a valid option")

        if test != False:
            choice = 'q'
        return choice


def menu_edit(entry, test=False, test_item=None):
    choice = None
    entry_id = entry.id
    while choice != 'q':
        print("Enter 'q' to return to the previous menu.")
        display(Entry.select().where(Entry.id == entry_id)[0])
        if test == False:
            choice = input("What would you like to edit? ").lower()
        else:
            choice = test
        clear()

        if choice == 'task':
            print("Task: {}".format(entry.task))
            if test_item == None:
                new_item = inputter('task', input("> "))
            else:
                new_item = test_item
            q = Entry.update(task=new_item).where(Entry.id == entry_id)
            q.execute()
        elif choice == 'duration':
            print("Duration: {}".format(entry.duration))
            if test_item == None:
                new_item = inputter('duration', input("(Must be an integer): "))
            else:
                new_item = test_item
            q = Entry.update(duration=new_item).where(Entry.id == entry_id)
            q.execute()
        elif choice == 'notes':
            print("Notes: {}".format(entry.notes))
            if test_item == None:
                new_item = inputter('notes', input("> "))
            else:
                new_item = test_item
            q = Entry.update(notes=new_item).where(Entry.id == entry_id)
            q.execute()
        elif choice == 'date':
            print("Date: {}".format(entry.timestamp))
            if test_item == None:
                new_item = inputter('date', input("(mm/dd/yyyy): "))
            else:
                new_item = test_item
            q = Entry.update(timestamp=new_item).where(Entry.id == entry_id)
            q.execute()
        elif choice == 'q':
            clear()
            pass
        else:
            print("I'm sorry, I can't let you do that.")
            print("\n\n")

        if test != False:
            choice = 'q'
    return choice


def add_entry(name, task, duration, notes):
    """Add an entry."""

    Entry.create(name=name, task=task, duration=duration, notes=notes)
    print("Entry successfully created.")


def delete_entry(entry):
    """Delete an entry."""
    entry.delete_instance()
    print("Entry deleted.")
    return True


def display(entry):
    """Displays entry information"""
    print("Name: {}".format(entry.name))
    print("Task: {}".format(entry.task))
    print("Duration: {}".format(entry.duration))
    print("Notes: {}".format(entry.notes))
    print("Date: {}".format(entry.timestamp.strftime('%A %B %d, %Y')))


def find_by_employee(query):
    """Find all entries from an employee."""
    return Entry.select().where(Entry.name.contains(query)).order_by(Entry.timestamp.desc())


def find_by_duration(query):
    """Find all entries with a specific duration."""
    return Entry.select().where(Entry.duration == query).order_by(Entry.timestamp.desc())


def find_by_term(query):
    """Find all entries pertaining to a term."""
    return Entry.select().where(
        Entry.task.contains(query) |
        Entry.notes.contains(query)).order_by(Entry.timestamp.desc())


def find_by_range(lower_date, higher_date):
    """Find all entries in a range of dates."""
    return Entry.select().where((Entry.timestamp >= lower_date) &
                                   (Entry.timestamp <= higher_date)).order_by(
                                   Entry.timestamp.desc())


def validate_date(string):
    try:
        var = datetime.datetime.strptime(string, "%m/%d/%Y").date()
        return True, var
    except ValueError:
        print("Invalid date.")
        return False


def validate_duration(string):
    try:
        var = int(string)
        return True
    except ValueError:
        print("That's not an integer.")
        return False


def inputter(select, choice):
    hold = False
    if select == 'menu':
        choice = choice.lower().strip()
    elif select == 'name':
        choice = choice.title()
    elif select == 'task':
        choice = choice
    elif select == 'duration':
        while hold == False:
            hold = validate_duration(choice)
            if hold == False:
                choice = input("Please enter an integer: ")
    elif select == 'notes':
        choice = choice
    elif select == 'date':
        while hold == False:
            hold, choice = validate_date(choice)
            if hold == False:
                choice = input("Please use the correct format (mm/dd/yyyy): ")
    elif select == 'query':
        choice = choice
    elif select == 'delete':
        choice = choice.lower()
    elif select == 'entry':
        while hold == False:
            choice = choice
            if choice == 'q':
                hold = True
            else:
                hold = validate_duration(choice)
            if hold == False:
                choice = input("Please choose an entry (number): ")
    clear()
    return choice


if __name__ == '__main__':
    initialize()
    menu_loop()
