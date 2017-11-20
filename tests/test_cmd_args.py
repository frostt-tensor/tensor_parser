#!/usr/bin/env python3

import unittest
import argparse

import tests
from tensor_parser import cmd_args

class TestCSVParser(unittest.TestCase):

  def test_positionals(self):
    myargs = ['1.csv', '2.csv', 'out.tns']
    args = cmd_args.parse_args(myargs)
    self.assertEqual(len(args.csv), 2)
    self.assertEqual(args.csv[0], '1.csv')
    self.assertEqual(args.csv[1], '2.csv')
    self.assertEqual(args.tensor, 'out.tns')

  def test_delim(self):
    myargs = ['1.csv', '2.csv', 'out.tns', '-F|']
    args = cmd_args.parse_args(myargs)
    self.assertEqual(args.field_sep, '|')

  def test_delim(self):
    myargs = ['1.csv', '2.csv', 'out.tns', '-f2', '-fname']
    args = cmd_args.parse_args(myargs)
    self.assertEqual(len(args.field), 2)
    self.assertEqual(args.field[0], '2')
    self.assertEqual(args.field[1], 'name')

  def test_sort(self):
    myargs = ['1.csv', '2.csv', 'out.tns', '-f2', '-fname', '-n2', '-lname']
    args = cmd_args.parse_args(myargs)
    self.assertEqual(len(args.sort_num), 1)
    self.assertEqual(args.sort_num[0], '2')
    self.assertEqual(len(args.sort_lex), 1)
    self.assertEqual(args.sort_lex[0], 'name')

  '''
  # Commented out because failed argparse prints to stderr, which is a pain...
  def test_missing(self):
    myargs = ['1.csv']
    try:
      args = cmd_args.parse_args(myargs)
    except:
      pass
  '''
    

if __name__ == '__main__':
    unittest.main()

