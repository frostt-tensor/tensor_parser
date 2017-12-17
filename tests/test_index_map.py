
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
    imap = index_map(type_func=index_map.TYPE_INT)
    imap.add(3)
    imap.add(2)
    imap.add(0)

    imap.build_map()

    self.assertEqual(imap[0], 1)
    self.assertEqual(imap[2], 2)
    self.assertEqual(imap[3], 3)


  def test_sort_flt(self):
    imap = index_map(type_func=index_map.TYPE_FLOAT)
    imap.add(3.2)
    imap.add(2.1)
    imap.add(2.5)

    imap.build_map()

    self.assertEqual(imap[2.1], 1)
    self.assertEqual(imap[2.5], 2)
    self.assertEqual(imap[3.2], 3)


  def test_sort_date(self):
    imap = index_map(type_func=index_map.TYPE_DATE)
    imap.add('07/01/1993')
    imap.add('1992')
    imap.add('01/01/99')
    imap.add('August 17th, 1111')

    imap.build_map()

    self.assertEqual(imap['08/17/1111'], 1)
    self.assertEqual(imap['1992'], 2)
    self.assertEqual(imap['July 1st, 1993'], 3)
    self.assertEqual(imap['01/01/99'], 4)



  def test_sort_date_year(self):
    imap = index_map(type_func=index_map.TYPE_DATE_YEAR)
    imap.add('07/01/1993')
    imap.add('1992')
    imap.add('1601')
    imap.add('01/01/99')

    imap.build_map()

    self.assertEqual(imap['1601'], 1)
    self.assertEqual(imap['1992'], 2)
    self.assertEqual(imap['1993'], 3)
    self.assertEqual(imap['1999'], 4)


  def test_sort_date_month(self):
    imap = index_map(type_func=index_map.TYPE_DATE_MONTH)
    imap.add('07/01/1993')
    imap.add('August')
    imap.add('June')
    imap.add('December')

    imap.build_map()

    self.assertEqual(imap['June'], 1)
    self.assertEqual(imap['July'], 2)
    self.assertEqual(imap['August'], 3)
    self.assertEqual(imap['December'], 4)


  def test_sort_date_hour(self):
    imap = index_map(type_func=index_map.TYPE_DATE_HOUR)
    imap.add('22:30')
    imap.add('1:00PM')

    imap.build_map()

    self.assertEqual(imap['13:00'], 1)
    self.assertEqual(imap['10:00PM'], 2)



if __name__ == '__main__':
    unittest.main()

