#!/usr/bin/env python3

import os, sys
import argparse
import pprint
import re

from functools import partial

# Make these available to eval() for user-defined types.
import datetime
from dateutil import parser as date_parser


# fix path nonsense: https://stackoverflow.com/a/6466139
if __name__ == '__main__' and __package__ is None:
  from sys import path
  from os.path import dirname as dir
  path.append(dir(path[0]))
  __package__ = 'scripts'


from tensor_parser.index_map import index_map
from tensor_parser.tensor_config import tensor_config
from tensor_parser.csv_parser import csv_parser
from tensor_parser.builder import build_tensor


#
# Helper functions
#
def roundf(ndigits):
  """ Returns a function that rounds floats with `ndigits` of precision. """
  def _roundf(ndigits, flt):
    return round(float(flt), ndigits)
  return partial(_roundf, ndigits)


def parse_types(cmd_args, config):
  """ Set mode types. Each --type flag gives us a string of field,field,..,func
  """
  builtin_funcs = {
    # index_map builtins
    'str'   : index_map.TYPE_STR,
    'int'   : index_map.TYPE_INT,
    'float' : index_map.TYPE_FLOAT,
    'date'  : index_map.TYPE_DATE,
    'year'  : index_map.TYPE_DATE_YEAR,
    'month' : index_map.TYPE_DATE_MONTH,
    'day'   : index_map.TYPE_DATE_DAY,
    'hour'  : index_map.TYPE_DATE_HOUR,
    'min'   : index_map.TYPE_DATE_MIN,
    'sec'   : index_map.TYPE_DATE_SEC,
  }
  for f in cmd_args:
    f = f.split(',')
    text_func = f[-1]

    func = None
    if text_func in builtin_funcs:
      func = builtin_funcs[text_func]
    else:
      # match function name and optional args that start after "-"
      # for example, "roundf-3" is transformed to "roundf(3)"
      func_re = '(?P<func_name>\w+)-(?P<func_args>[,\w]+)$'
      match = re.match(func_re, text_func)
      if match:
        func_name = match.group('func_name')
        func_args = match.group('func_args')
        text_func = '{}({})'.format(func_name, func_args)
      func = eval(text_func)

    for field in f[:-1]:
      print('field "{}" -> type "{}"'.format(field, text_func))
      config.set_mode_type(field, func)



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

    If no field is provided for tensor values ('--vals'), then a tensor of
    count data is constructed.

    TYPES
    =====
    You can change the type of one or multiple CSV fields with the '--type'
    flag. For example, '--type=userid,custid,int --type=sale,date' will treat
    the 'userid' and 'custid' fields as integers and the 'sale' field as a
    date.

      Available types:
        str      => string (default)
        int      => integer
        float    => float
        roundf-X => round a float to X digits
        date     => calendar date (supports year, month, day, hour, seconds)
        year     => extract year from date
        month    => extract month from date
        day      => extract day from date
        hour     => extract hour from date
        min      => extract minute from date
        sec      => extract second from date

    ADVANCED: if the provided field is not in the above list, it is interpreted
    as a custom type and converted to source code. See README.md for details.
  '''
  parser = argparse.ArgumentParser(description=my_description,
      formatter_class=argparse.RawTextHelpFormatter)

  #
  # Required positional arguments
  #
  parser.add_argument('csv', type=str, nargs='+',
      help='CSV files to parse')
  parser.add_argument('tensor', type=str,
      help='output tensor file (.tns)')

  #
  # Adding and modifying tensor modes
  #
  parser.add_argument('-f', '--field', type=str, action='append',
      help='include FIELD as tensor mode')
  parser.add_argument('--vals', type=str,
      help='the field to use for values')

  parser.add_argument('--no-sort', type=str, metavar='FIELD', action='append',
      help="do not sort FIELD")
  parser.add_argument('-t', '--type', type=str, metavar='FIELDS,TYPE',
      action='append', help="treat FIELDs as type TYPE. See --help for details")

  #
  # CSV configuration
  #
  parser.add_argument('-F', '--field-sep', type=str,
      help='CSV field separator (default: auto)')
  parser.add_argument('--has-header', choices=['yes', 'no'],
      help='Indicate whether CSV has a header row (default: auto)')

  parser.add_argument('-q', '--query', action='store_true',
      help='query metadata of the CSV file and exit')

  parser.add_argument('--merge', type=str, default='sum',
      choices=['none', 'sum', 'min', 'max', 'avg', 'count'],
      help='function for merging duplicate non-zeros (default: sum)')

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

  # Check for file query
  if args.query:
    parser = csv_parser(args.csv[0])
    print('Found delimiter: "{}"'.format(parser.get_delimiter()))
    print('Found fields:')
    pprint.pprint(parser.get_header())
    sys.exit(0)


  # fill in lists if not present
  if not args.field:
    print('WARN: tensor has no modes specified.', file=sys.stderr)
    args.field = []
  if not args.no_sort:
    args.no_sort = []
  if not args.type:
    args.type = []


  # Build tensor configuration
  config = tensor_config(csv_names=cmd_args.csv, tensor_name=cmd_args.tensor)
  config.set_delimiter(cmd_args.field_sep)
  config.set_header(cmd_args.has_header)
  for f in cmd_args.field:
    config.add_mode(f)

  for f in cmd_args.no_sort:
    config.set_mode_sort(f, False)

  merge_funcs = {
    'none' : tensor_config.MERGE_NONE,
    'sum'  : tensor_config.MERGE_SUM,
    'min'  : tensor_config.MERGE_MIN,
    'max'  : tensor_config.MERGE_MAX,
    'avg'  : tensor_config.MERGE_AVG,
    'count': tensor_config.MERGE_COUNT,
  }
  if args.merge:
    config.set_merge_func(merge_funcs[args.merge])

  parse_types(cmd_args.type, config)

  config.set_vals(cmd_args.vals)

  return config


if __name__ == '__main__':
  config = parse_args()
  build_tensor(config)


