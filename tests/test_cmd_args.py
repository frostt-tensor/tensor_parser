
import unittest
import argparse
from contextlib import redirect_stdout

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
    self.assertEqual(config.get_mode_by_idx(0)['field'], '1')
    self.assertEqual(config.get_mode_by_idx(0)['sort'], True)

  def test_delim(self):
    myargs = ['1.csv', '2.csv', 'out.tns', '-F|', '-f1']
    config = build_tensor.parse_args(myargs)
    self.assertEqual(config.get_delimiter(), '|')

  def test_fields(self):
    myargs = ['1.csv', '2.csv', 'out.tns', '-f2', '-fuser']
    config = build_tensor.parse_args(myargs)
    self.assertEqual(config.num_modes(), 2)
    self.assertEqual(config.get_mode_by_idx(0)['field'], '2')
    self.assertEqual(config.get_mode_by_idx(1)['field'], 'user')
    self.assertEqual(config.get_mode_by_idx(0)['sort'], True)
    self.assertEqual(config.get_mode_by_idx(1)['sort'], True)

  def test_vals(self):
    myargs = ['hi.csv', 'out.tns', '-f1', '--vals=ratings']
    config = build_tensor.parse_args(myargs)
    self.assertEqual(config.get_vals(), 'ratings')

  def test_header(self):
    myargs = ['hi.csv', 'out.tns', '-f1']
    config = build_tensor.parse_args(myargs)
    self.assertEqual(config.has_header(), None)

    myargs = ['hi.csv', 'out.tns', '-f1', '--has-header=yes']
    config = build_tensor.parse_args(myargs)
    self.assertEqual(config.has_header(), True)

    myargs = ['hi.csv', 'out.tns', '-f1', '--has-header=no']
    config = build_tensor.parse_args(myargs)
    self.assertEqual(config.has_header(), False)


  def test_type_int(self):
    myargs = ['hi.csv', 'out.tns', '-f1', '--type=1,int']

    with open(os.devnull, 'w') as redirect:
      with redirect_stdout(redirect):
        config = build_tensor.parse_args(myargs)
    f = config.get_mode('1')['type']
    self.assertEqual(f('138'), 138)


  def test_type_roundf(self):
    myargs = ['hi.csv', 'out.tns', '-f1', '--type=1,roundf-1']

    with open(os.devnull, 'w') as redirect:
      with redirect_stdout(redirect):
        config = build_tensor.parse_args(myargs)
    f = config.get_mode('1')['type']
    self.assertEqual(f('1.38'), 1.4)

if __name__ == '__main__':
    unittest.main()

