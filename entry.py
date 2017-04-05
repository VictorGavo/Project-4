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


def menu_loop():
    """Show the menu."""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit.")

        for key, value in main_menu.items():
            print('[{}] {}'.format(key, value))
        choice = input("Action: ").lower().strip()
        clear()

        if choice == 'a':
            name = input("Name: ").title()
            task = input("Task: ")
            duration = validator('int')
            notes = input("Notes: ")
            add_entry(name, task, duration, notes)
        elif choice == 'l':
            menu_lookup()


def menu_lookup():
    """Lookup entries."""
    choice = None

    while choice != 'q':
        print("Enter 'q' to return to the previous menu.")
        for key, value in lookup_menu.items():
            print('[{}] {}'.format(key, value))
        choice = input('Action: ').lower().strip()
        clear()

        if choice == 'd':
            menu_date()
        elif choice == 'e':
            query = input("Enter a name: ").capitalize()
            find_by_employee(query)
        elif choice == 't':
            query = input("Enter a term: ")
            find_by_term(query)


def menu_date():
    """Lookup entries by date."""
    choice = None

    while choice != 'q':
        print("Enter 'q' to return to the previous menu.")
        for key, value in date_menu.items():
            print('[{}] {}'.format(key, value))
        choice = input('Action: ').lower().strip()
        clear()

        if choice == 'a':
            list_entries(Entry.select().order_by(Entry.timestamp.desc()))
        elif choice == 'r':
            lower_date = validator('date')
            higher_date = validator('date')
            find_by_range(lower_date, higher_date)


def menu_edit(choice):
    if choice == 'task':
        item = input("Task: ")
    elif choice == 'duration':
        item = validator('int')
    elif choice == 'notes':
        item = input("Notes: ")
    elif choice == 'date':
        item = validator('date')
    elif choice == 'quit':
        item = 0
    return item


def add_entry(name, task, duration, notes):
    """Add an entry."""

    Entry.create(name=name, task=task, duration=duration, notes=notes)
    clear()


def delete_entry(entry):
    """Delete an entry."""
    if input("Are you sure? [yN] ").lower() == 'y':
        entry.delete_instance()
        print("Entry deleted.")


def edit_entry(choice, entry, new_item):
    """Edit the current entry."""
    entry_id = entry.id

    if choice == 'task':
        q = Entry.update(task=new_item).where(Entry.id == entry_id)
        q.execute()
    elif choice == 'duration':
        q = Entry.update(duration=new_item).where(Entry.id == entry_id)
        q.execute()
    elif choice == 'notes':
        q = Entry.update(notes=new_item).where(Entry.id == entry_id)
        q.execute()
    elif choice == 'date':
        q = Entry.update(timestamp=new_item).where(Entry.id == entry_id)
        q.execute()
    elif choice == 'quit':
        pass
    else:
        print("That is not a valid command.")


def entry_options(entries, index):
    """Look through a list of entries."""
    action = None
    entry = entries[index]
    display(entry)
    print("\n\n")
    print("[e] edit entry")
    print("[d] delete entry")
    try:
        entries[index-1]
        print("[p] previous entry")
    except ValueError:
        pass
    try:
        entries[index+1]
        print("[n] next entry")
    except IndexError:
        pass
    print("[q] return to main menu")

    action = input("Action: ").lower().strip()

    if action == 'e':
        clear()
        display(entry)
        choice = validator('edit')
        new_item = menu_edit(choice)
        edit_entry(choice, entry, new_item)
    elif action == 'd':
        delete_entry(entries[index])
        clear()
    elif action == 'p':
        try:
            entries[index-1]
            index -= 1
            clear()
            entry_options(entries, index)
        except ValueError:
            clear()
            print("This is the first entry.")
            entry_options(entries, index)
    elif action == 'n':
        try:
            entries[index+1]
            index += 1
            clear()
            entry_options(entries, index)
        except IndexError:
            clear()
            print("This is the last entry.")
            entry_options(entries, index)
    elif action == 'q':
        clear()
        pass


def display(entry):
    """Displays entry information"""
    print("Name: {}".format(entry.name))
    print("Task: {}".format(entry.task))
    print("Duration: {}".format(entry.duration))
    print("Notes: {}".format(entry.notes))
    print("Date: {}".format(entry.timestamp.strftime('%A %B %d, %Y')))


def find_by_employee(query):
    """Find all entries from an employee."""
    entries = Entry.select().where(Entry.name.contains(query)).order_by(Entry.timestamp.desc())
    list_entries(entries)


def find_by_term(query):
    """Find all entries pertaining to a term."""
    entries = Entry.select().where(
        Entry.task.contains(query) |
        Entry.notes.contains(query)).order_by(Entry.timestamp.desc())
    list_entries(entries)


def find_by_range(lower_date, higher_date):
    """Find all entries in a range of dates."""
    entries = Entry.select().where((Entry.timestamp >= lower_date) &
                                   (Entry.timestamp <= higher_date)).order_by(
                                   Entry.timestamp.desc())
    list_entries(entries)


def list_entries(entries):
    count = 0
    if entries:
        for entry in entries:
            count += 1
            print("[{}] {}, {}".format(count, entry.name, entry.task))

        next_action = input("Select an entry: ")
        clear()
        try:
            int(next_action)
            index = int(next_action) - 1
            entry_options(entries, index)
        except ValueError:
            if next_action != 'q':
                print("That is an invalid command.")
            pass
    else:
        print("No entries were found that match your search criteria.")


def validator(var):
    """Takes input from the user and calls the appropriate function"""
    hold = 0
    if var == 'int':
        while hold == 0:
            duration = input("Duration (in minutes): ")
            try:
                val = int(duration)
                return duration
            except ValueError:
                print("That's not an integer.")
    elif var == 'date':
        while hold == 0:
            date = input("Enter a date (mm/dd/yyyy): ")
            try:
                date = datetime.datetime.strptime(date, "%m/%d/%Y").date()
                return date
            except ValueError:
                print("Invalid date.")
    elif var == 'edit':
        choice_bank = ['task', 'duration', 'notes', 'date']
        choice = input("What would you like to edit? ").lower()
        while choice not in choice_bank:
            print("That is not a valid option.")
            choice = input("What would you like to edit? ").lower()
        return choice


main_menu = OrderedDict([
    ('a', "Add an entry."),
    ('l', "Lookup entries."),
])

lookup_menu = OrderedDict([
    ('e', "Find all entries from an employee."),
    ('d', "Lookup entries by date."),
    ('t', "Find all entries pertaining to a term."),
])

date_menu = OrderedDict([
    ('r', "Find all entries in a range of dates."),
    ('a', "List all entries by date.")
])

if __name__ == '__main__':
    initialize()
    menu_loop()
