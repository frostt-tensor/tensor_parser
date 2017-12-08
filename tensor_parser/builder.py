
from .index_map import index_map
from .tensor_config import tensor_config
from .csv_parser import csv_parser


def build_tensor(config):
  print('building from {}'.format(config.get_inputs()))
  indmaps = []
  for m in range(config.num_modes()):
    mode_sort = config.get_mode(m)['sort']
    indmaps.append(index_map(sort=mode_sort))

  for fin in config.get_inputs():
    # build CSV parser
    parser = csv_parser(fin, config.get_delimiter(), config.has_header())

    # First determine which columns to extract
    cols = [0] * config.num_modes()
    header = parser.get_header()
    for m in range(config.num_modes()):
      field = config.get_mode(m)['field']
      cols[m] = header.index(field)

    for row in parser.rows():
      print(row[cols[0]], row[cols[1]])
      break
