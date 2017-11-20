

import argparse


def parse_args(cmd_args=None):
  my_description = '''
    Construct a tensor from CSV-like files. The files can either be in plain
    text form or compressed (.gz or .bz2).

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
      help="sort a fields's keys numerically")


  #
  # Other configuration
  #
  parser.add_argument('-F', '--field-sep', type=str, default=',',
      help='CSV field separator (default: ",")')

  if cmd_args is not None:
    # parse provided args
    return parser.parse_args(cmd_args)
  else:
    # parse sys.argv
    return parser.parse_args()

