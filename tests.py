import unittest

from entry import *


class EntryTests(unittest.TestCase):

    def test_add_entry(self):
        name = 'Test Name'
        task = 'Test Task'
        duration = 10
        notes = 'Test Notes go here.'

        entry = Entry.create(name=name, task=task, duration=duration, notes=notes)
        self.assertIn(entry, Entry.select())


if __name__ == '__main__':
    unittest.main()
