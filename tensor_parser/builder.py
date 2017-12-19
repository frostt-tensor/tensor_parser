
import os
import sys
import uuid # for filenames
from ast import literal_eval # safely eval literals during merge
from contextlib import redirect_stdout
from csvsorter import csvsort

from .index_map import index_map
from .tensor_config import tensor_config
from .csv_parser import csv_parser


def grab_cols(parser, config):
  """ Map the modes of the tensor to column indices in the CSV file.

  Args:
    parser (csv_parser): The CSV file of interest.
    config (tensor_config): Configuration for the tensor to construct
  """
  num_modes = config.num_modes() # save some typing
  header = [x.lower() for x in parser.get_header()]
  cols = []
  for m in range(num_modes):
    field = config.get_mode_by_idx(m)['field']
    if field.lower() not in header:
      print('ERROR: field "{}" not found in {}'.format(field, fin),
          file=sys.stderr)
      sys.exit(1)
    cols.append(header.index(field.lower()))
  return cols


def merge_dups(tensor_name, num_modes, merge_func=sum):
  """ Remove duplicate non-zeros from a tensor file. """
  sorted_f = tensor_name + '.sorted'
  tmp_name = str(uuid.uuid4().hex) + '.tns'
  try:
    # Sort the "CSV" tensor -- this library prints to stdout in old versions,
    # so suppress that
    with open(os.devnull, 'w') as redirect:
      with redirect_stdout(redirect):
        csvsort(tensor_name, range(num_modes), output_filename=sorted_f,
            max_size=800, delimiter=' ', has_header=False)

    # Merge duplicate non-zeros
    with open(tmp_name, 'w') as fout:
      dup_lines = []
      with open(sorted_f, 'r') as fin:
        for line in fin:
          line = line.split()

          # indices do not match -- merge previous duplicates
          if len(dup_lines) > 0 and line[:-1] != dup_lines[0][:-1]:
            vals = [literal_eval(x[-1]) for x in dup_lines]
            inds = [str(x) for x in dup_lines[0][:-1]]
            print('{} {}'.format(' '.join(inds), merge_func(vals)), file=fout)
            dup_lines = []

          dup_lines.append(line)

      # final flush
      vals = [eval(x[-1]) for x in dup_lines]
      inds = [str(x) for x in dup_lines[0][:-1]]
      print('{} {}'.format(' '.join(inds), merge_func(vals)), file=fout)

      # overwrite original data
      os.rename(tmp_name, tensor_name)

  except:
    # if there was an exception, we don't want to overwrite the original data
    os.remove(tmp_name)

  finally:
    os.remove(sorted_f)



def build_tensor(config):
  num_modes = config.num_modes() # save some typing

  indmaps = []
  for m in range(num_modes):
    m_type = config.get_mode_by_idx(m)['type']
    sort_  = config.get_mode_by_idx(m)['sort']
    name_ = config.get_mode_by_idx(m)['field']
    indmaps.append(index_map(name=name_, type_func=m_type, sort=sort_))

  #
  # Build index maps
  #
  for fin in config.get_inputs():
    # build CSV parser
    parser = csv_parser(fin, config.get_delimiter(), config.has_header())

    cols = grab_cols(parser, config)

    #
    # Go over each row to build index maps
    #
    for row in parser.rows():
      for m in range(num_modes):
        indmaps[m].add(row[cols[m]])


  # First pass over the data is now complete. However due to pruning of
  # indices, we have to make a second pass. Suppose a key i was pruned. If a
  # key in another mode (j) only appeared when i was found, then j must also be
  # pruned.
  for fin in config.get_inputs():
    parser = csv_parser(fin, config.get_delimiter(), config.has_header())
    cols = grab_cols(parser, config)

    # Go over each row and remove unused keys
    for row in parser.rows():
      pruned = False
      for m in range(num_modes):
        if indmaps[m].get_count(row[cols[m]]) < 1:
          pruned = True
          break
      if pruned:
        for m in range(num_modes):
          indmaps[m].sub(row[cols[m]])

  for m in range(num_modes):
    indmaps[m].build_map()

  #
  # Now go back over the data and build the tensor
  #
  with open(config.get_output(), 'w') as fout:
    for fin in config.get_inputs():
      parser = csv_parser(fin, config.get_delimiter(), config.has_header())
      cols = grab_cols(parser, config)

      #
      # Go over each row to build index maps
      #
      inds = [0] * num_modes

      # optionally extract values
      val_field = config.get_vals()
      val_col = -1
      if val_field:
        val_col = parser.get_header().index(val_field)

      # Grab indices and prune non-zeros with None indices
      val = 1
      for row in parser.rows():
        pruned = False
        for m in range(num_modes):
          idx = indmaps[m][row[cols[m]]]
          if idx:
            inds[m] = str(idx)
          else:
            pruned = True

        if val_col != -1:
          val = row[val_col]

        if not pruned:
          print('{} {}'.format(' '.join(inds), val), file=fout)

  # may be None to leave duplicates
  if config.get_merge_func():
    merge_dups(config.get_output(), num_modes,
        merge_func=config.get_merge_func())

  #
  # Write maps to file
  #
  for m in range(num_modes):
    fieldname = config.get_mode_by_idx(m)['field'].replace(' ', '')
    indmaps[m].write_file('mode-{}-{}.map'.format(m+1,fieldname))


