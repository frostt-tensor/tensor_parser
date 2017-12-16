
import unittest

import tests
from tensor_parser.index_map import index_map

class TestCSVParser(unittest.TestCase):

  def test_sub(self):
    imap = index_map()
    imap.add('banana')
    imap.add('apple')
    imap.add('apple')

    self.assertEqual(imap.get_count('banana'), 1)
    self.assertEqual(imap.get_count('apple'), 2)
    imap.sub('apple')
    self.assertEqual(imap.get_count('apple'), 1)
    imap.sub('apple')
    self.assertEqual(imap.get_count('apple'), 0)
    

  def test_sort_none(self):
    imap = index_map(sort=False)
    imap.add('banana')
    imap.add('apple')
    imap.add('0')

    self.assertFalse(imap.is_mapped())
    imap.build_map()
    self.assertTrue(imap.is_mapped())

    self.assertEqual(imap['banana'], 1)
    self.assertEqual(imap['apple'], 2)
    self.assertEqual(imap['0'], 3)


  def test_sort_lex(self):
    imap = index_map()
    imap.add('banana')
    imap.add('apple')
    imap.add(0)

    imap.build_map()

    self.assertEqual(imap[0], 1)
    self.assertEqual(imap['apple'], 2)
    self.assertEqual(imap['banana'], 3)


  def test_sort_int(self):
    imap = index_map(type_func=int)
    imap.add(3)
    imap.add(2)
    imap.add(0)

    imap.build_map()

    self.assertEqual(imap[0], 1)
    self.assertEqual(imap[2], 2)
    self.assertEqual(imap[3], 3)


  def test_sort_flt(self):
    imap = index_map(type_func=float)
    imap.add(3.2)
    imap.add(2.1)
    imap.add(2.5)

    imap.build_map()

    self.assertEqual(imap[2.1], 1)
    self.assertEqual(imap[2.5], 2)
    self.assertEqual(imap[3.2], 3)





if __name__ == '__main__':
    unittest.main()

