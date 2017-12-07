

from .index_map import index_map

class tensor_config:
  def __init__(self, csv_names=None, tensor_name=None):
    """ An intermediate representation of user configuration information.
    
    Any front-end such as a command-line or GUI should construct one of these
    objects and provide to a `tensor_parser` object.

    Args:
      csv_names (list): The list of CSV files to parse.
      tensor_name (str): The name of the output file.
    """

    self._inputs = csv_names
    self._output = tensor_name

    # defaults
    self._field_sep = None
    self._modes = []
    self._vals = None


  def set_delimiter(self, delim):
    """ Specify the delimiter in the CSV file(s).
    
    This will override whichever delimiter is detected automatically.
    """
    self._field_sep = delim

  def get_delimiter(self):
    """ Return the user-specified CSV delimiter. Returns None if unspecified.
    """
    return self._field_sep


  def add_mode(self, csv_field, sort_policy=index_map.SORT_NONE):
    """ Add a mode to the tensor.

    Args:
      csv_field (str): Which field of the CSV to use
      sort (func): See `set_mode_sort()`
    """
    mode = dict()
    mode['field'] = csv_field
    mode['sort']  = sort_policy
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


  def set_mode_sort(self, csv_field, sort_policy):
    """ Set the sorting policy for a mode.

    The sorting policy will ultimately be supplied to an `index_map`. This
    should be a function which transforms a string key to another type before
    sorting.  For example:

      set_mode_sort('user_ids', lambda x : int(x))

    will sort the mode defined by user_ids by their integer representations.
    Several predefined ones are provided in the `index_map` class. The above
    example could be accomplished via:

      set_mode_sort('user_ids', index_map.SORT_INT)

    If `csv_field` does not specify a mode which has been added via
    `add_mode()`, this function raises an IndexError.

    Args:
      csv_field (str): Which field of the CSV to modify
      sort_policy (func): A function which converts the key before `sorted()`
    """

    for idx in range(len(self._modes)):
      if self._modes[idx]['field'] == csv_field:
        self._modes[idx]['sort'] = sort_policy
        return
    raise IndexError("Error: field '{}' not found.".format(csv_field))


  def get_mode_sort(self, csv_field):
    """Return the sorting policy for a mode.

    If `csv_field` does not specify a mode which has been added via
    `add_mode()`, this function raises an IndexError.

    Args:
      csv_field (str): Which field of the CSV to query
    """
    for idx in range(len(self._modes)):
      if self._modes[idx]['field'] == csv_field:
        return self._modes[idx]['sort']
    raise IndexError("Error: field '{}' not found.".format(csv_field))


  def get_mode(self, mode_idx):
    """ Return the dictionary representing meta-data for mode `mode_idx`.
    
    The dictionary will take the form:
      {
        csv_field => one of the columns in the CSV file
        sort      => sorting policy
      }

    Args:
      mode_idx (int): Which mode of the tensor to query (zero-indexed)
    """
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



