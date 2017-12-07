
import unittest
import argparse

import tests
from tensor_parser.index_map import index_map
from tensor_parser.tensor_config import tensor_config

class TestTensorConfig(unittest.TestCase):

  def test_delim(self):
    config = tensor_config()
    config.set_delimiter('|')
    self.assertEqual(config.get_delimiter(), '|')

  def test_inputs(self):
    config = tensor_config(csv_names=['1.csv', '2.csv'])
    inputs = config.get_inputs()
    self.assertEqual(inputs[0], '1.csv')
    self.assertEqual(inputs[1], '2.csv')

    config.add_input('3.csv')
    inputs = config.get_inputs()
    self.assertEqual(inputs[2], '3.csv')

  def test_mode_order(self):
    config = tensor_config()
    config.add_mode('one')
    config.add_mode('two')
    self.assertEqual(config.get_mode(0)['field'], 'one')
    self.assertEqual(config.get_mode(1)['field'], 'two')
    self.assertEqual(config.num_modes(), 2)


  def test_sort(self):
    config = tensor_config()
    # no sort by default
    config.add_mode('item_ids')
    self.assertEqual(config.get_mode_sort('item_ids'), index_map.SORT_NONE)

    # change sort
    config.set_mode_sort('item_ids', index_map.SORT_LEX)
    self.assertEqual(config.get_mode_sort('item_ids'), index_map.SORT_LEX)

    # set sort from beginning
    config.add_mode('user_ids', index_map.SORT_INT)
    self.assertEqual(config.get_mode_sort('user_ids'), index_map.SORT_INT)
    func = config.get_mode_sort('user_ids')
    self.assertEqual(func('1'), 1)

    # custom sort
    config.set_mode_sort('user_ids', lambda x: 1138)
    func = config.get_mode_sort('user_ids')
    self.assertEqual(func('hi'), 1138)


if __name__ == '__main__':
    unittest.main()

