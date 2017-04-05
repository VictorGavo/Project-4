import unittest
import sys
from test import support


from entry import *


class EntryTests(unittest.TestCase):

    def test_add_entry(self):
        name = 'Test Name'
        task = 'Test Task'
        duration = 1
        notes = 'Test Notes Go Here.'
        add_entry(name=name, task=task, duration=duration, notes=notes)
        entries = Entry.select().where(Entry.name == name)
        self.assertGreater(len(entries), 0)


    def test_edit_entry(self):
        entries = Entry.select().where(Entry.name == 'Test Name')
        entry = entries[0]
        new_task = "EDITED"
        edit_entry(choice="task", entry=entry, new_item=new_task)
        entries = Entry.select().where(Entry.name == 'Test Name')
        entry = entries[0]
        self.assertEqual(entry.task, new_task)

        entries = Entry.select().where(Entry.name == 'Test Name')
        entry = entries[0]
        new_duration = 88
        edit_entry(choice="duration", entry=entry, new_item=new_duration)
        entries = Entry.select().where(Entry.name == 'Test Name')
        entry = entries[0]
        self.assertEqual(entry.duration, new_duration)

        entries = Entry.select().where(Entry.name == 'Test Name')
        entry = entries[0]
        new_notes = 'VICTOR WUZ HERE!!1!'
        edit_entry(choice="notes", entry=entry, new_item=new_notes)
        entries = Entry.select().where(Entry.name == 'Test Name')
        entry = entries[0]
        self.assertEqual(entry.notes, new_notes)

        entries = Entry.select().where(Entry.name == 'Test Name')
        entry = entries[0]
        new_date = datetime.datetime.strptime('10/31/1991', "%m/%d/%Y").date()
        edit_entry(choice="date", entry=entry, new_item=new_date)
        entries = Entry.select().where(Entry.name == 'Test Name')
        entry = entries[0]
        self.assertEqual(entry.timestamp, new_date)

        entries = Entry.select().where(Entry.name == 'Test Name')
        entry = entries[0]
        new_date = datetime.datetime.strptime('10/31/1992', "%m/%d/%Y").date()
        edit_entry(choice="quit", entry=entry, new_item=new_date)
        entries = Entry.select().where(Entry.name == 'Test Name')
        entry = entries[0]
        self.assertNotEqual(entry.timestamp, new_date)

    # def test_initialize(self):

    def test_delete_entry(self):
        Entry.create(name='Marmaduke', task='bloopity blah', duration=88, notes='Wubba Lubba Dub Dub')
        entries_before = Entry.select().where(Entry.name == 'Marmaduke')
        entry = entries_before[0]
        delete_entry(entry)
        entries_after = Entry.select().where(Entry.name == 'Marmadukes')
        self.assertLess(entries_after, entries_before)

        # entries = Entry.select()
        # for entry in entries:
        #     entry.delete_instance()

    # def test_entry_options(self):
    #     index = 0
    #     entries = Entry.select()
    #
    # def test_list_entries(self):
    #     entries = Entry.select()

    def test_display(self):

        display(Entry.select()[0])
        assert stdout.getvalue()



if __name__ == '__main__':
    unittest.main()
