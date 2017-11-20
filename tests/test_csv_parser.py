#!/usr/bin/env python3

import unittest

import os

import tests
from tensor_parser import csv_parser

class TestCSVParser(unittest.TestCase):

  def test_delim(self):
    path = os.path.join(tests.DATA_DIR, 'test.csv')
    p = csv_parser.csv_parser(path)
    self.assertEqual(p.delim(), ',')

if __name__ == '__main__':
    unittest.main()

