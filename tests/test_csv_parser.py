
import unittest

import os
import uuid

import tests
from tensor_parser import csv_parser

class TestCSVParser(unittest.TestCase):

  def test_delim(self):
    tmp_name = str(uuid.uuid4().hex) + '.csv'
    try:
      # make csv
      with open(tmp_name, 'w') as fout:
        print('1,2,3,1.0', file=fout)
        print('1,2,3,1.0', file=fout)
        print('1,2,3,1.0', file=fout)
      p = csv_parser.csv_parser(tmp_name)
      self.assertEqual(p.get_delimiter(), ',')
      self.assertEqual(p.get_header(), ['1', '2', '3', '4'])
    finally:
      os.remove(tmp_name)

  def test_gzip(self):
    tmp_name = str(uuid.uuid4().hex) + '.csv.gz'
    try:
      # make csv
      with csv_parser.open_file(tmp_name, 'w') as fout:
        print('1,2,3,1.0', file=fout)
        print('1,2,3,1.0', file=fout)
        print('1,2,3,1.0', file=fout)
      p = csv_parser.csv_parser(tmp_name)
      self.assertEqual(p.get_delimiter(), ',')
      self.assertEqual(p.num_columns(), 4)
      for row in p.rows():
        self.assertEqual(row, ['1', '2', '3', '1.0'])
    finally:
      os.remove(tmp_name)


  def test_bz2(self):
    tmp_name = str(uuid.uuid4().hex) + '.csv.bz2'
    try:
      # make csv
      with csv_parser.open_file(tmp_name, 'w') as fout:
        print('1,2,3,1.0', file=fout)
        print('1,2,3,1.0', file=fout)
        print('1,2,3,1.0', file=fout)
      p = csv_parser.csv_parser(tmp_name)
      self.assertEqual(p.get_delimiter(), ',')
      self.assertEqual(p.num_columns(), 4)
      for row in p.rows():
        self.assertEqual(row, ['1', '2', '3', '1.0'])
    finally:
      os.remove(tmp_name)


  def test_default_header(self):
    tmp_name = str(uuid.uuid4().hex) + '.tmp'
    try:
      # make csv
      with open(tmp_name, 'w') as fout:
        print('1 2 3 1.0', file=fout)
        print('1 2 3 1.0', file=fout)
        print('1 2 3 1.0', file=fout)
      p = csv_parser.csv_parser(tmp_name)
      self.assertEqual(p.get_header(), ['1', '2', '3', '4'])
    finally:
      os.remove(tmp_name)


  def test_header(self):
    tmp_name = str(uuid.uuid4().hex) + '.tmp'
    try:
      # make csv
      with open(tmp_name, 'w') as fout:
        print('1 2 3 2.0', file=fout) # "will be header"
        print('1 2 3 1.0', file=fout)
        print('1 2 3 1.0', file=fout)
        print('1 2 3 1.0', file=fout)
      p = csv_parser.csv_parser(tmp_name, has_header=True)
      self.assertEqual(p.get_delimiter(), ' ')
      self.assertEqual(p.num_columns(), 4)
      for row in p.rows():
        self.assertEqual(row, ['1', '2', '3', '1.0'])
    finally:
      os.remove(tmp_name)


if __name__ == '__main__':
    unittest.main()

