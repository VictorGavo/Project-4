import functools
import unittest
from unittest.mock import patch
import sys
from test.support import captured_stdin, captured_stdout


from entry import *


class EntryTests(unittest.TestCase):

    def setUp(self):
        # self.test_bank = ["Test Name", "Test Task", 1, "Test Notes Go Here."]
        self.entry = Entry.create(name="Test Name", task="Created during setUp", duration=1, notes="Test Notes Go Here.")


    def tearDown(self):
        entries = Entry.select()
        for entry in entries:
            entry.delete_instance()


    def test_menu_loop_q(self):
        self.assertEqual(menu_loop(test='q'), 'q')

    def test_menu_lookup_q(self):
        self.assertEqual(menu_lookup(test='q'), 'q')

    def test_menu_date_q(self):
        self.assertEqual(menu_date(test='q'), 'q')

    def test_menu_list_not_option(self):
        self.assertEqual(menu_list('all', 'test', test='88'), 'q')

    def test_menu_list_else(self):
        self.assertEqual(menu_list('employee', 'Mertin', test='q'), 'None')

    def test_menu_list_search_by(self):
        self.assertEqual(menu_list(None, 'Mertin', test='q'), 'q')

    def test_menu_list_quit(self):
        self.assertEqual(menu_list('all', 'test', test='q'), 'q')

    def test_menu_entry_previous(self):
        Entry.create(name="Test Name", task="Created during menu_entry tests", duration=1, notes="Test Notes Go Here.")
        self.assertEqual(menu_entry(Entry.select(), 1, test='p'), 'q')

    def test_menu_entry_next(self):
        Entry.create(name="Test Name", task="Also created during menu_entry tests", duration=1, notes="Test Notes Go Here.")
        self.assertEqual(menu_entry(Entry.select(), 0, test='n'), 'q')

    def test_menu_entry_error(self):
        self.assertEqual(menu_entry(Entry.select(), 0, test='test'), 'q')

    def test_menu_edit_task(self):
        self.assertEqual(
                menu_edit(Entry.select()[0], test='task', test_item='test item'), 'q')

    def test_menu_edit_duration(self):
        self.assertEqual(
                menu_edit(Entry.select()[0], test='duration', test_item='10'), 'q')

    def test_menu_edit_notes(self):
        self.assertEqual(
                menu_edit(Entry.select()[0], test='notes', test_item='test item'), 'q')

    def test_menu_edit_date(self):
        self.assertEqual(
                menu_edit(Entry.select()[0], test='date', test_item='10/31/1991'), 'q')

    def test_menu_edit_else(self):
        self.assertEqual(
                menu_edit(Entry.select()[0], test='boogers', test_item='test item'), 'q')

    def test_menu_edit_q(self):
        self.assertEqual(menu_edit(Entry.select()[0], test='q'), 'q')

    def test_get_entries_all(self):
        self.assertEqual(get_entries('all', None), Entry.select())

    def test_get_entries_employee(self):
        query = 'test'
        result = Entry.select().where(Entry.name.contains(query))
        self.assertEqual(get_entries('employee', 'test'), result)

    def test_get_entries_term(self):
        query = 'test'
        result = Entry.select().where(Entry.task.contains(query) |
                                      Entry.notes.contains(query))
        self.assertEqual(get_entries('term', 'test'), result)

    def test_get_entries_duration(self):
        query = '1'
        result = Entry.select().where(Entry.duration == query)
        self.assertEqual(get_entries('duration', '1'), result)

    def test_get_entries_range(self):
        query= [datetime.date(1991, 10, 31), datetime.date(1991, 11, 1)]
        result = Entry.select().where((Entry.timestamp >= query[0]) &
                                      (Entry.timestamp <= query[1])).order_by(
                                       Entry.timestamp.desc())
        self.assertEqual(get_entries('range', query), result)

    def test_delete_entry(self):
        test_entry = Entry.create(name='Rick Sanchez', task='pooperschkooper', duration=42, notes='j;askdlfjk;lasdfjk;adfjk')
        delete_entry(Entry.select().where(Entry.name == 'Rick Sanchez')[0])
        entries_after = Entry.select()
        self.assertNotIn(test_entry, entries_after)

    def test_validate_date(self):
        self.assertTrue(validate_date('10/31/1991'))

    def test_validate_date_fail(self):
        self.assertFalse(validate_date("Bob's Burgers"))

    def test_validate_duration(self):
        self.assertTrue(validate_duration("10"))

    def test_validate_duration_fail(self):
        self.assertFalse(validate_duration("Gareth (Said with disdain)"))

    def test_inputter_menu(self):
        self.assertEqual(inputter('menu', '   B   '), 'b')

    def test_inputter_name(self):
        self.assertEqual(inputter('name', 'victor'), 'Victor')

    def test_inputter_task(self):
        self.assertEqual(inputter('task', '   B   '), '   B   ')

    def test_inputter_duration(self):
        self.assertEqual(inputter('duration', '10'), '10')

    def test_inputter_notes(self):
        self.assertEqual(inputter('notes', '   B   '), '   B   ')

    def test_inputter_date(self):
        self.assertEqual(inputter('date', '10/31/1991'), datetime.date(1991, 10, 31))

    def test_inputter_query(self):
        self.assertEqual(inputter('query', '   B   '), '   B   ')

    def test_inputter_delete(self):
        self.assertEqual(inputter('delete', 'B'), 'b')

    def test_inputter_entry_q(self):
        self.assertEqual(inputter('entry', 'q'), 'q')

    def test_inputter_entry_valid(self):
        self.assertEqual(inputter('entry', '8'), '8')






    # def test_menu_list_20(self):
    #     self.assertEqual(menu_list('all', 'test', test=20), '20')
    #     # The way things are set up passing anything but 'q' results in infinite loop

    # def test_menu_loop_q(self):
    #     self.assertEqual(menu_loop(test='a'), 'a')
    #     # Needs captured_stdin, captured_stdout

    # def test_menu_loop_q(self):
    #     self.assertEqual(menu_loop(test='l'), 'l')
    #     # DOESNT NEED TO BE TESTED

    def test_add_entry(self):
        entries_before = Entry.select().where(Entry.name == "Test Name")
        add_entry(name="Test Name", task="Created with add_entry", duration=1, notes="Test Notes Go Here.")
        entries_after = Entry.select().where(Entry.name == "Test Name")
        self.assertGreater(entries_after, entries_before)



if __name__ == '__main__':
    unittest.main()
