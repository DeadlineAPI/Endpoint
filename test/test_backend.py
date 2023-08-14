import unittest
import os

import backend

class TestBackend(unittest.TestCase):
    def test_db_connection(self):
        conn = backend.get_db(os.path.join('test','endpoint.db'))
        self.assertTrue( not conn is None )
        conn.close()

    def test_reset_and_initialize(self):
        backend.reset_database(os.path.join('test','endpoint.db'))
        conn = backend.get_db(os.path.join('test','endpoint.db'))
        self.assertTrue(not conn is None)
        conn.close()

    def test_initialize(self):
        backend.reset_database(os.path.join('test','endpoint.db'))
        conn = backend.get_db(os.path.join('test','endpoint.db'))
        conn.close()

    def test_add_entry(self):
        backend.reset_database(os.path.join('test','endpoint.db'))
        conn = backend.get_db(os.path.join('test','endpoint.db'))
        backend.add_entry(conn, dict( name="test", deadline="test", startdate="test"))
        l = backend.get_entries(conn)
        self.assertTrue(len(l) == 1)
        conn.close()

    def test_delete_entry(self):
        backend.reset_database(os.path.join('test','endpoint.db'))
        conn = backend.get_db(os.path.join('test','endpoint.db'))
        backend.add_entry(conn, dict( name="test", deadline="test", startdate="test"))
        l = backend.get_entries(conn)
        self.assertTrue(len(l) == 1)
        backend.delete_entry(conn, l[0]["id"])
        l = backend.get_entries(conn)
        self.assertTrue(len(l) == 0)
        conn.close()

    def test_edit_entry(self):
        backend.reset_database(os.path.join('test','endpoint.db'))
        conn = backend.get_db(os.path.join('test','endpoint.db'))
        backend.add_entry(conn, dict( name="test", deadline="test", startdate="test"))
        l = backend.get_entries(conn)
        self.assertTrue(l[0]["name"] == "test")
        self.assertTrue(l[0]["shortname"] == None)
        entry = {**l[0], "name": "a good test"}
        backend.edit_entry(conn, entry, id=entry["id"])
        l = backend.get_entries(conn)
        self.assertTrue(l[0]["name"] == "a good test")
        self.assertTrue(l[0]["shortname"] == None)
        conn.close()