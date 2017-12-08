#!/usr/bin/env python3

import os, sys
import argparse
import pprint

# fix path nonsense: https://stackoverflow.com/a/6466139
if __name__ == '__main__' and __package__ is None:
  from sys import path
  from os.path import dirname as dir
  path.append(dir(path[0]))
  __package__ = 'bin'


from tensor_parser.index_map import index_map
from tensor_parser.tensor_config import tensor_config
from tensor_parser.csv_parser import csv_parser
from tensor_parser.builder import build_tensor


def parse_args(cmd_args=None):
  my_description = '''
    Construct a tensor from CSV-like files. The files can either be in plain
    text form or compressed (.gz or .bz2).

    Fields can be specified by their name if the CSV file has a header, or
    otherwise can be specified with a 1-indexed integer corresponding to their
    column in the CSV file.

    The field separator and CSV header can often be automatically detected.
    Use the '--query' flag to determine what is automatically detected. For
    example, '--query=header' will print the list of discovered CSV fields.

    If no field is provided for tensor values ('--vals'), then a binary tensor
    is constructed.
  '''
  parser = argparse.ArgumentParser(description=my_description,
      formatter_class=argparse.RawTextHelpFormatter)

  #
  # Required positional arguments
  #
  parser.add_argument('csv', type=str, nargs='+', help='CSV files to parse')
  parser.add_argument('tensor',  type=str, help='output tensor file (.tns)')

  #
  # Adding and modifying tensor modes
  #
  parser.add_argument('-f', '--field', type=str, action='append',
      help='include FIELD as tensor mode')
  parser.add_argument('--vals', type=str,
      help='the field to use for values')

  parser.add_argument('-l', '--sort-lex', type=str, action='append',
      help="sort a fields's keys lexicographically")
  parser.add_argument('-n', '--sort-num', type=str, action='append',
      help="sort a fields's integer keys")


  #
  # CSV configuration
  #
  parser.add_argument('-F', '--field-sep', type=str,
      help='CSV field separator (default: auto)')
  parser.add_argument('--has-header', choices=['yes', 'no'],
      help='Indicate whether CSV has a header row (default: auto)')

  parser.add_argument('-q', '--query', action='append',
      choices=['field-sep', 'header'],
      help='print the header found in the CSV file and exit')


  #
  # Parse arguments.
  #
  args = None
  if cmd_args is not None:
    # parse provided args
    args = cmd_args=parser.parse_args(cmd_args)
  else:
    # parse sys.argv
    args = cmd_args=parser.parse_args()

  if args.has_header:
    if args.has_header == 'yes':
      args.has_header = True
    else:
      args.has_header = False

  #
  # Check for file query.
  #
  if args.query:
    parser = csv_parser(args.csv[0])
    for query in args.query:
      if query == 'field-sep':
        print('Found delimiter: "{}"'.format(parser.get_delimiter()))
      if query == 'header':
        print('Found fields:')
        pprint.pprint(parser.get_header())
    sys.exit(0)



  # fill in lists if not present
  if not args.field:
    print('WARN: tensor has no modes specified.', file=sys.stderr)
    args.field = []
  if not args.sort_lex:
    args.sort_lex = []
  if not args.sort_num:
    args.sort_num = []

  # Build tensor configuration
  config = tensor_config(csv_names=cmd_args.csv, tensor_name=cmd_args.tensor)
  config.set_delimiter(cmd_args.field_sep)
  config.set_header(cmd_args.has_header)
  for f in cmd_args.field:
    config.add_mode(f)
  for f in cmd_args.sort_lex:
    config.set_mode_sort(f, index_map.SORT_LEX)
  for f in cmd_args.sort_num:
    config.set_mode_sort(f, index_map.SORT_INT)
  config.set_vals(cmd_args.vals)

  return config



if __name__ == '__main__':
  config = parse_args()
  build_tensor(config)


