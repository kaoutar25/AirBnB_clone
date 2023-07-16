#!/usr/bin/python3
"""
Test for storage
"""
from datetime import datetime
import unittest
from time import sleep
import json
import os
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.__init__ import storage
import pep8


class test_fileStorage(unittest.TestCase):
    """Test FileStorage Class"""
    def test_instances(self):
        """chequeamos instantation"""
        obj = FileStorage()
        self.assertIsInstance(obj, FileStorage)

    def test_docstrings(self):
        """Test docstrings"""
        self.assertIsNotNone(FileStorage.__doc__)

    def test_docs(self):
        """Test documentation"""
        self.assertIsNotNone(FileStorage.all.__doc__)
        self.assertIsNotNone(FileStorage.new.__doc__)
        self.assertIsNotNone(FileStorage.save.__doc__)
        self.assertIsNotNone(FileStorage.reload.__doc__)
        self.assertTrue(FileStorage.all.__doc__)
        self.assertTrue(FileStorage.new.__doc__)
        self.assertTrue(FileStorage.save.__doc__)
        self.assertTrue(FileStorage.reload.__doc__)

    def test_all_method_contains_dict_of_base_model_objects(self):
        """FileStorage all method contains dict of BaseModel objs"""
        storage = FileStorage()
        storage_dict = storage.all()
        self.assertIsInstance(storage_dict, dict)
        for obj in storage_dict.values():
            self.assertIsInstance(obj, BaseModel)

    def test_new_method_adds_object_to_storage(self):
        """FileStorage new method adds object"""
        base = BaseModel()
        storage = FileStorage()
        storage_dict = storage.all()
        key = '{}.{}'.format(type(base).__name__, base.id)
        self.assertTrue(key in storage_dict.keys())

    def test_save_method_updates_objects_and_file(self):
        """FileStorage save method updates __objects

        Test if file already exists.
        with self.assertRaises(FileNotFoundError):
            open('file.json', 'r')
        """
        bm = BaseModel()
        key = '{}.{}'.format(type(bm).__name__, bm.id)
        bm_updated_0 = bm.updated_at
        storage = FileStorage()
        obj = storage.all()
        dict_1 = obj[key].updated_at

        sleep(0.0001)
        bm.save()

        bm_updated_1 = bm.updated_at
        obj2 = storage.all()
        dict_2 = obj2[key].updated_at

        self.assertNotEqual(bm_updated_1, bm_updated_0)
        self.assertNotEqual(dict_2, dict_1)

        try:
            with open('file.json', 'r'):
                os.remove('file.json')
        except FileNotFoundError:
            self.assertEqual(1, 2)

    def test_pycodestyle_file_storage(self):
        """Test that we conform to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")


if __name__ == '__main__':
    unittest.main()
