
from .index_map import index_map
from .tensor_config import tensor_config
from .csv_parser import csv_parser


def build_tensor(config):
  num_modes = config.num_modes() # save some typing

  indmaps = []
  for m in range(num_modes):
    mode_sort = config.get_mode(m)['sort']
    indmaps.append(index_map(sort=mode_sort))

  #
  # Build index maps
  #
  for fin in config.get_inputs():
    # build CSV parser
    parser = csv_parser(fin, config.get_delimiter(), config.has_header())

    # First determine which columns to extract
    cols = []
    header = parser.get_header()
    for m in range(num_modes):
      field = config.get_mode(m)['field']
      cols.append(header.index(field))

      print(header[cols[-1]])

    print(cols)

    #
    # Go over each row to build index maps
    #
    for row in parser.rows():
      for m in range(num_modes):
        indmaps[m].add(row[cols[m]])

  for m in range(num_modes):
    indmaps[m].build_map()

  #
  # Now go back over the data and build the tensor
  #
  with open(config.get_output(), 'w') as fout:
    for fin in config.get_inputs():
      # build CSV parser
      parser = csv_parser(fin, config.get_delimiter(), config.has_header())

      # grab column indices
      cols = [0] * num_modes
      header = parser.get_header()
      for m in range(num_modes):
        field = config.get_mode(m)['field']
        cols[m] = header.index(field)

      #
      # Go over each row to build index maps
      #
      inds = [0] * num_modes

      # optionally extract values
      val_field = config.get_vals()
      val_col = -1
      if val_field:
        val_col = parser.get_header().index(val_field)

      val = 1
      for row in parser.rows():
        for m in range(num_modes):
          inds[m] = str(indmaps[m][row[cols[m]]])

        if val_col != -1:
          val = row[val_col]

        print('{} {}'.format(' '.join(inds), val), file=fout)




  # Write maps to file
  for m in range(num_modes):
    indmaps[m].write_file(
        'mode-{}-{}.map'.format(m+1,config.get_mode(m)['field']))


