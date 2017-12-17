
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
    self.assertEqual(config.get_mode_by_idx(0)['field'], 'one')
    self.assertEqual(config.get_mode_by_idx(1)['field'], 'two')
    self.assertEqual(config.num_modes(), 2)

  def test_get_mode(self):
    config = tensor_config()
    config.add_mode('mode')
    config.set_mode_sort('mode', False)
    mode = config.get_mode('mode')
    self.assertEqual(mode['field'], 'mode')
    self.assertEqual(mode['type']('138'), '138')
    self.assertEqual(mode['sort'], False)


  def test_sort(self):
    config = tensor_config()
    # no sort by default
    config.add_mode('item_ids')
    m = config.get_mode_by_idx(0)
    self.assertEqual(m['sort'], True)

    # change sort
    config.set_mode_sort('item_ids', False)
    m = config.get_mode_by_idx(0)
    self.assertEqual(m['sort'], False)


if __name__ == '__main__':
    unittest.main()

