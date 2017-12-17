

from .index_map import index_map

class tensor_config:

  MERGE_NONE  = None
  MERGE_SUM   = sum
  MERGE_MIN   = min
  MERGE_MAX   = max
  MERGE_AVG   = (lambda l : float(sum(l)) / len(l))
  MERGE_COUNT = len

  def __init__(self, csv_names=None, tensor_name=None):
    """ An intermediate representation of user configuration information.

    Any front-end such as a command-line or GUI should construct one of these
    objects and provide to a `builder` object.

    Args:
      csv_names (list): The list of CSV files to parse.
      tensor_name (str): The name of the output file.
    """

    self._inputs = csv_names
    self._output = tensor_name

    # defaults
    self._field_sep = None
    self._has_header = None
    self._modes = []
    self._vals = None
    self._merge_func = sum


  def set_delimiter(self, delim):
    """ Specify the delimiter in the CSV file(s).

    This will override whichever delimiter is detected automatically.

    Args:
      delim (str): The delimiter to use in the CSV files.
    """
    self._field_sep = delim


  def get_delimiter(self):
    """ Return the user-specified CSV delimiter. Returns None if unspecified.
    """
    return self._field_sep


  def set_header(self, has_header):
    """ Indicate whether the input CSVs have a header row.

    This will override the header that is automatically detected.

    Args:
      has_header (bool): Whether the CSVs have a header as the first row
    """
    self._has_header = has_header


  def has_header(self):
    """ Return bool indicating whether CSVs should have a header row. """
    return self._has_header


  def add_mode(self, csv_field, transform=index_map.TYPE_STR, sort=True):
    mode = dict()
    mode['field'] = csv_field
    mode['type']  = transform
    mode['sort']  = sort
    self._modes.append(mode)


  def set_vals(self, csv_field):
    """ Set the field of the CSV file to use as the tensor values.

    Args:
      csv_field (str): Which field of the CSV to use as the values.
    """
    self._vals = csv_field


  def get_vals(self):
    """ Return the field of the CSV file to use as the tensor values.  """
    return self._vals


  def set_mode_sort(self, csv_field, to_sort):
    assert(isinstance(to_sort, bool))
    for idx in range(self.num_modes()):
      if self._modes[idx]['field'].lower() == csv_field.lower():
        self._modes[idx]['sort'] = to_sort
        return
    raise IndexError("Error: field '{}' not found.".format(csv_field))


  def set_mode_type(self, csv_field, type_func):
    """ Set the type of a mode.

    The mode type will ultimately be supplied to an `index_map`. This should be
    a function which transforms a string key to another type before sorting.
    For example:

      set_mode_type('user_ids', lambda x : int(x))

    will type of the mode defined by user_ids by their integer representations.
    Several predefined ones are provided in the `index_map` class. The above
    example could be accomplished via:

      set_mode_type('user_ids', index_map.TYPE_INT)

    If `csv_field` does not specify a mode which has been added via
    `add_mode()`, this function raises an IndexError.

    Args:
      csv_field (str): Which field of the CSV to modify
      mode_type (func): A function which converts the key before `sorted()`
    """

    for idx in range(len(self._modes)):
      if self._modes[idx]['field'].lower() == csv_field.lower():
        self._modes[idx]['type'] = type_func
        return
    raise IndexError("Error: field '{}' not found.".format(csv_field))


  def set_merge_func(self, merge_func):
    self._merge_func = merge_func

  def get_merge_func(self):
    return self._merge_func

  def get_mode(self, csv_field):
    """ Return the dictionary representing meta-data for a mode.

    NOTE: `csv_field` is case insensitive.

    The dictionary will take the form:
      {
        field => one of the columns in the CSV file
        type  => function for setting type (func)
        sort  => sorting policy (bool)
      }

    Args:
      csv_field (str): Which mode of the tensor to query.
    """
    for idx in range(self.num_modes()):
      if self._modes[idx]['field'].lower() == csv_field.lower():
        return self._modes[idx]
    raise IndexError("Error: field {} not found.".format(csv_field))


  def get_mode_by_idx(self, mode_idx):
    """ Return the dictionary representing meta-data for mode `mode_idx`.

    The dictionary will take the form:
      {
        field => one of the columns in the CSV file
        type  => function for setting type (func)
        sort  => sorting policy (bool)
      }

    Args:
      mode_idx (int): Which mode of the tensor to query (zero-indexed)
    """
    if mode_idx >= self.num_modes():
      raise IndexError("Error: mode {} not found.".format(mode_idx))
    return self._modes[mode_idx]


  def add_input(self, csv_file):
    """ Add a file to the list of inputs.

    Args:
      csv_file (str): The name of the CSV file
    """
    self._inputs.append(csv_file)


  def get_inputs(self):
    """ Return the list of input CSV files.  """
    return self._inputs


  def set_output(self, filename):
    """ Set the name of the output tensor name.

    Args:
      filename (str): The name of the output file
    """
    self._output = filename


  def get_output(self):
    """ Return the output filename.  """
    return self._output


  def num_modes(self):
    """ Return the number of modes in the tensor.  """
    return len(self._modes)



