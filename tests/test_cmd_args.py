
import unittest
import argparse

import os, sys
sys.path.append(os.path.abspath('..'))

import tests
from scripts import build_tensor

from tensor_parser.index_map import index_map

class TestCSVParser(unittest.TestCase):

  def test_positionals(self):
    myargs = ['1.csv', '2.csv', 'out.tns', '-f1']
    config = build_tensor.parse_args(myargs)

    self.assertEqual(len(config.get_inputs()), 2)
    self.assertEqual(config.get_inputs()[0], '1.csv')
    self.assertEqual(config.get_inputs()[1], '2.csv')

    self.assertEqual(config.get_output(), 'out.tns')

    self.assertEqual(config.num_modes(), 1)
    self.assertEqual(config.get_mode(0)['field'], '1')
    self.assertEqual(config.get_mode(0)['sort'], index_map.SORT_NONE)

  def test_delim(self):
    myargs = ['1.csv', '2.csv', 'out.tns', '-F|', '-f1']
    config = build_tensor.parse_args(myargs)
    self.assertEqual(config.get_delimiter(), '|')

  def test_fields(self):
    myargs = ['1.csv', '2.csv', 'out.tns', '-f2', '-fuser']
    config = build_tensor.parse_args(myargs)
    self.assertEqual(config.num_modes(), 2)
    self.assertEqual(config.get_mode(0)['field'], '2')
    self.assertEqual(config.get_mode(1)['field'], 'user')
    self.assertEqual(config.get_mode(0)['sort'], index_map.SORT_NONE)
    self.assertEqual(config.get_mode(1)['sort'], index_map.SORT_NONE)

  def test_sort(self):
    myargs = ['1.csv', '2.csv', 'out.tns', '-f2', '-fuser', '-n2', '-luser']
    config = build_tensor.parse_args(myargs)
    self.assertEqual(config.get_mode(0)['sort'], index_map.SORT_INT)
    self.assertEqual(config.get_mode(1)['sort'], index_map.SORT_LEX)

  def test_vals(self):
    myargs = ['hi.csv', 'out.tns', '-f1', '--vals=ratings']
    config = build_tensor.parse_args(myargs)
    self.assertEqual(config.get_vals(), 'ratings')

if __name__ == '__main__':
    unittest.main()

