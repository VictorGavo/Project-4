from collections import OrderedDict
import datetime
from datetime import date
import os
import sys

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
            print('[{}] {}'.format(key, value.__doc__))
        choice = input("Action: ").lower().strip()
        clear()

        if choice in main_menu:
            main_menu[choice]()


def menu_lookup():
    """Lookup entries."""
    choice = None

    while choice != 'q':
        print("Enter 'q' to return to the previous menu.")
        for key, value in lookup_menu.items():
            print('[{}] {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()
        clear()

        if choice in lookup_menu:
            lookup_menu[choice]()


def menu_date():
    """Lookup entries by date."""
    choice = None

    while choice != 'q':
        print("Enter 'q' to return to the previous menu.")
        for key, value in date_menu.items():
            print('[{}] {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()
        clear()

        if choice in date_menu:
            date_menu[choice]()


def find_by_employee():
    """Find all entries from an employee."""
    query = input("Enter a name: ").capitalize()
    entries = Entry.select().where(Entry.name == query).order_by(Entry.timestamp.desc())
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
            view_entry(entries, index)
        except ValueError:
            print("That is an invalid command.")
            pass
    else:
        print("No entries were found that match your search criteria.")


def find_by_term():
    """Find all entries pertaining to a term."""
    query = input("Enter a term: ")
    entries = Entry.select().where(
        Entry.task.contains(query) |
        Entry.notes.contains(query)).order_by(Entry.timestamp.desc())
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
            view_entry(entries, index)
        except ValueError:
            print("That is an invalid command.")
            pass
    else:
        print("No entries were found that match your search criteria.")


def find_by_range():
    """Find all entries in a range of dates."""
    lower_date = input("Enter the earlier date (mm/dd/yyyy): ")
    higher_date = input("Enter the later date (mm/dd/yyyy): ")
    try:
        lower_date = datetime.datetime.strptime(lower_date, "%m/%d/%Y").date()
        higher_date = datetime.datetime.strptime(higher_date, "%m/%d/%Y").date()
    except ValueError:
        print("Invalid dates.")
    entries = Entry.select().where((Entry.timestamp >= lower_date) &
                                   (Entry.timestamp <= higher_date)).order_by(Entry.timestamp.desc())
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
            view_entry(entries, index)
        except ValueError:
            print("That is an invalid command.")
            pass
    else:
        print("No entries were found that match your search criteria.")


def all_entries():
    """List all entries by date."""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    count = 0

    if entries:
        for entry in entries:
            count += 1
            print("[{}] {}, {}".format(count, entry.name, entry.task))

        next_action = input("Select an entry: ")
        clear()
        if next_action == 'q':
            pass
        elif int(next_action):
            index = int(next_action) - 1
            view_entry(entries, index)
    else:
        print("It appears there are no entries.")


def view_entry(entries, index):
    """Look through a list of entries."""
    action = None
    display(entries[index])
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
        editor(entries[index])
    elif action == 'd':
        delete_entry(entries[index])
        clear()
    elif action == 'p':
        try:
            entries[index-1]
            index -= 1
            clear()
            view_entry(entries, index)
        except ValueError:
            clear()
            print("This is the first entry.")
            view_entry(entries, index)
    elif action == 'n':
        try:
            entries[index+1]
            index += 1
            clear()
            view_entry(entries, index)
        except IndexError:
            clear()
            print("This is the last entry.")
            view_entry(entries, index)
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


def add_entry():
    """Add an entry."""
    name = input("Name: ").capitalize()
    task = input("Task: ")
    duration = input("Duration (in minutes): ")
    notes = input("Notes: ")

    Entry.create(name=name, task=task, duration=duration, notes=notes)
    clear()


def delete_entry(entry):
    """Delete an entry."""
    if input("Are you sure? [yN] ").lower() == 'y':
        entry.delete_instance()
        print("Entry deleted.")


def editor(entry):
    """Edit the current entry."""
    entry_id = entry.id
    display(entry)
    choice = input("What would you like to edit? ").lower()

    if choice == 'task':
        q = Entry.update(task=input("New Task: ")).where(Entry.id == entry_id)
        q.execute()
    elif choice == 'duration':
        q = Entry.update(duration=input("New Duration (in minutes): ")).where(Entry.id == entry_id)
        q.execute()
    elif choice == 'notes':
        q = Entry.update(notes=input("New Notes: ")).where(Entry.id == entry_id)
        q.execute()
    elif choice == 'date':
        var = input("New Date (mm/dd/yyyy): ")
        var = datetime.datetime.strptime(var, "%m/%d/%Y")
        q = Entry.update(timestamp=var).where(Entry.id == entry_id)
        q.execute()
    elif choice == 'quit':
        pass
    else:
        print("That is not a valid command.")



main_menu = OrderedDict([
    ('a', add_entry),
    ('l', menu_lookup),
])

lookup_menu = OrderedDict([
    ('e', find_by_employee),
    ('d', menu_date),
    ('t', find_by_term),
])

date_menu = OrderedDict([
    ('r', find_by_range),
    ('a', all_entries)
])

if __name__ == '__main__':
    initialize()
    menu_loop()
