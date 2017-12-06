
import unittest
import argparse

import tests
from tensor_parser import cmd_args
from tensor_parser.index_map import index_map

class TestCSVParser(unittest.TestCase):

  def test_positionals(self):
    myargs = ['1.csv', '2.csv', 'out.tns', '-f1']
    config = cmd_args.parse_args(myargs)
    self.assertEqual(len(config.inputs()), 2)
    self.assertEqual(config.inputs()[0], '1.csv')
    self.assertEqual(config.inputs()[1], '2.csv')
    self.assertEqual(config.output(), 'out.tns')

  def test_delim(self):
    myargs = ['1.csv', '2.csv', 'out.tns', '-F|', '-f1']
    config = cmd_args.parse_args(myargs)
    self.assertEqual(config.delimiter(), '|')

  def test_fields(self):
    myargs = ['1.csv', '2.csv', 'out.tns', '-f2', '-fuser']
    config = cmd_args.parse_args(myargs)
    self.assertEqual(config.num_modes(), 2)
    self.assertEqual(config.mode(0)['csv_field'], '2')
    self.assertEqual(config.mode(1)['csv_field'], 'user')
    self.assertEqual(config.mode(0)['sort'], index_map.SORT_NONE)
    self.assertEqual(config.mode(1)['sort'], index_map.SORT_NONE)

  def test_sort(self):
    myargs = ['1.csv', '2.csv', 'out.tns', '-f2', '-fuser', '-n2', '-luser']
    config = cmd_args.parse_args(myargs)
    self.assertEqual(config.mode(0)['sort'], index_map.SORT_INT)
    self.assertEqual(config.mode(1)['sort'], index_map.SORT_LEX)


if __name__ == '__main__':
    unittest.main()

