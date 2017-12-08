
import unittest

import os

import tests
from tensor_parser import csv_parser

class TestCSVParser(unittest.TestCase):

  def test_delim(self):
    path = os.path.join(tests.DATA_DIR, 'test.csv')
    p = csv_parser.csv_parser(path)
    self.assertEqual(p.get_delimiter(), ',')

if __name__ == '__main__':
    unittest.main()

