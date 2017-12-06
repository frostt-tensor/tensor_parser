

import sys
import argparse
from tensor_parser.index_map import index_map


class csv_config:
  '''
    A class providing structure to the command-line arguments. This defines
    tensor modes, their respective fields in the CSV file(s), etc.
  '''

  def __init__(self, cmd_args):
    self._inputs = cmd_args.csv
    self._output = cmd_args.tensor
    self._field_sep = cmd_args.field_sep

    self._modes = []
    if cmd_args.field is None:
      print("ERROR: no fields from CSV specified. Re-run with '--help'")
      sys.exit(1)

    # construct mode dictionaries
    for f in cmd_args.field:
      self._modes.append(
        {
          'csv_field' : f,
          'sort'      : index_map.SORT_NONE,
        }
      )

    # Set non-default sort values
    if cmd_args.sort_num:
      for field_name in cmd_args.sort_num:
        for x in self._modes:
          if x['csv_field'] == field_name:
            x['sort'] = index_map.SORT_INT
    if cmd_args.sort_lex:
      for field_name in cmd_args.sort_lex:
        for x in self._modes:
          if x['csv_field'] == field_name:
            x['sort'] = index_map.SORT_LEX



  def mode(self, mode_idx):
    '''
      Return the dictionary representing meta-data for mode `mode_idx`. The
      dictionary will take the form:
      {
        csv_field => one of the columns in the CSV file
        sort      => one of the appropriate `index_map.SORT_XXX` values
      }
    '''
    return self._modes[mode_idx]

  def delimiter(self):
    '''
      User-specified CSV delimiter. `None` if unspecified.
    '''
    return self._field_sep

  def inputs(self):
    '''
      Return the list of input CSV files.
    '''
    return self._inputs

  def output(self):
    '''
      The output filename.
    '''
    return self._output


  def num_modes(self):
    '''
      Return the number of modes in the tensor.
    '''
    return len(self._modes)



def parse_args(cmd_args=None):
  my_description = '''
    Construct a tensor from CSV-like files. The files can either be in plain
    text form or compressed (.gz or .bz2).

    Fields can be specified by their name if the CSV file has a header, or
    otherwise can be specified with a 1-indexed integer corresponding to their
    column in the CSV file.

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
    return csv_config(parser.parse_args(cmd_args))
  else:
    # parse sys.argv
    return csv_config(parser.parse_args())

