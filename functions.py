from collections import OrderedDict
import datetime
from datetime import date
import os
import sys

import entry
from peewee import *


# def find_by_employee(query):
#     """Find all entries from an employee."""
#     entries = Entry.select().where(Entry.name == query).order_by(Entry.timestamp.desc())
#     count = 0
#
#     if entries:
#         for entry in entries:
#             count += 1
#             print("[{}] {}, {}".format(count, entry.name, entry.task))
#
#         next_action = input("Select an entry: ")
#         clear()
#         try:
#             int(next_action)
#             index = int(next_action) - 1
#             entry_options(entries, index)
#         except ValueError:
#             print("That is an invalid command.")
#             pass
#     else:
#         print("No entries were found that match your search criteria.")
#
#
# def find_by_term():
#     """Find all entries pertaining to a term."""
#     query = input("Enter a term: ")
#     entries = Entry.select().where(
#         Entry.task.contains(query) |
#         Entry.notes.contains(query)).order_by(Entry.timestamp.desc())
#     count = 0
#
#     if entries:
#         for entry in entries:
#             count += 1
#             print("[{}] {}, {}".format(count, entry.name, entry.task))
#
#         next_action = input("Select an entry: ")
#         clear()
#         try:
#             int(next_action)
#             index = int(next_action) - 1
#             entry_options(entries, index)
#         except ValueError:
#             print("That is an invalid command.")
#             pass
#     else:
#         print("No entries were found that match your search criteria.")
#
#
# def find_by_range():
#     """Find all entries in a range of dates."""
#     lower_date = input("Enter the earlier date (mm/dd/yyyy): ")
#     higher_date = input("Enter the later date (mm/dd/yyyy): ")
#     try:
#         lower_date = datetime.datetime.strptime(lower_date, "%m/%d/%Y").date()
#         higher_date = datetime.datetime.strptime(higher_date, "%m/%d/%Y").date()
#     except ValueError:
#         print("Invalid dates.")
#     entries = Entry.select().where((Entry.timestamp >= lower_date) &
#                                    (Entry.timestamp <= higher_date)).order_by(Entry.timestamp.desc())
#     count = 0
#
#     if entries:
#         for entry in entries:
#             count += 1
#             print("[{}] {}, {}".format(count, entry.name, entry.task))
#
#         next_action = input("Select an entry: ")
#         clear()
#         try:
#             int(next_action)
#             index = int(next_action) - 1
#             entry_options(entries, index)
#         except ValueError:
#             print("That is an invalid command.")
#             pass
#     else:
#         print("No entries were found that match your search criteria.")
#
#
# def all_entries():
#     """List all entries by date."""
#     entries = Entry.select().order_by(Entry.timestamp.desc())
#     count = 0
#
#     if entries:
#         for entry in entries:
#             count += 1
#             print("[{}] {}, {}".format(count, entry.name, entry.task))
#
#         next_action = input("Select an entry: ")
#         clear()
#         if next_action == 'q':
#             pass
#         elif int(next_action):
#             index = int(next_action) - 1
#             entry_options(entries, index)
#     else:
#         print("It appears there are no entries.")
