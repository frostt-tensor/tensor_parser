
import unittest
import argparse

import os, sys
import uuid
sys.path.append(os.path.abspath('..'))

import tests
from tensor_parser import builder

class TestBuilder(unittest.TestCase):

  def test_merge_default(self):
    tmp_name = str(uuid.uuid4().hex) + '.tmp'
    try:
      # make csv
      with open(tmp_name, 'w') as fout:
        print('1 2 3 1.0', file=fout)
        print('1 2 3 1.0', file=fout)

      builder.merge_dups(tmp_name, 3)

      with open(tmp_name, 'r') as fin:
        lines = fin.readlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0].strip(), '1 2 3 2.0')

    finally:
      os.remove(tmp_name)


  def test_merge_max(self):
    tmp_name = str(uuid.uuid4().hex) + '.tmp'
    try:
      # make csv
      with open(tmp_name, 'w') as fout:
        print('1 2 3 1.0', file=fout)
        print('1 2 3 5.0', file=fout)

      builder.merge_dups(tmp_name, 3, reduce_func=max)

      with open(tmp_name, 'r') as fin:
        lines = fin.readlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0].strip(), '1 2 3 5.0')

    finally:
      os.remove(tmp_name)


  def test_merge_more(self):
    tmp_name = str(uuid.uuid4().hex) + '.tmp'
    try:
      # make csv
      with open(tmp_name, 'w') as fout:
        print('1 2 3 1.0', file=fout)
        print('2 1 3 2.0', file=fout)
        print('1 2 3 5.0', file=fout)

      builder.merge_dups(tmp_name, 3, reduce_func=sum)

      with open(tmp_name, 'r') as fin:
        lines = fin.readlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0].strip(), '1 2 3 6.0')
        self.assertEqual(lines[1].strip(), '2 1 3 2.0')

    finally:
      os.remove(tmp_name)


  def test_merge_huge(self):
    N = 2000000
    tmp_name = str(uuid.uuid4().hex) + '.tmp'
    try:
      # make csv
      with open(tmp_name, 'w') as fout:
        for i in range(N):
          print('1 2 3 1.0', file=fout)

      builder.merge_dups(tmp_name, 3, reduce_func=sum)

      with open(tmp_name, 'r') as fin:
        lines = fin.readlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0].strip(), '1 2 3 {:0.1f}'.format(N))

    finally:
      os.remove(tmp_name)


  def test_merge_custom(self):
    tmp_name = str(uuid.uuid4().hex) + '.tmp'
    try:
      # make csv
      with open(tmp_name, 'w') as fout:
        print('1 2 3 1.0', file=fout)
        print('1 2 3 1.0', file=fout)

      builder.merge_dups(tmp_name, 3, reduce_func=lambda x : -1)

      with open(tmp_name, 'r') as fin:
        lines = fin.readlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0].strip(), '1 2 3 -1')

    finally:
      os.remove(tmp_name)


