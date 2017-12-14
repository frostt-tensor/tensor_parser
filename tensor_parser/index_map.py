

import sys
from collections import OrderedDict

class index_map:
  """ Construct and maintain a mapping of strings to contiguous indices in a
  tensor.

  All keys are converted to strings (`str()`) before insertion/access. Indices
  start from 1.

  After all keys have been added with `add()`, the map to continuous indices
  must be built with `build_map()`. Mappings of keys -> indices can then be
  accessed with `__getitem__()` (i.e., `my_map['apple']` will return its index
  in the tensor).
  """

  def __init__(self, name, type_func='lamba x : x', sort=True):
    self._keys = OrderedDict()
    self._map  = dict()

    self._name = name

    self._type_func = type_func
    self._is_mapped = False
    self._sort = sort

    self.skipped = set()

  def __access_key(self, key):
    assert(isinstance(key, str))
    try:
      return self._type_func(key)
    except:
      return None


  def add(self, key):
    """ Increment the count of a key in index_map.
    """
    newkey = self.__access_key(key)
    if newkey is None:
      if key not in self.skipped:
        print('Mode {} skipping key: "{}"'.format(self._name, key),
            file=sys.stderr)
        self.skipped.add(key)
      return

    if newkey in self._keys:
      self._keys[newkey] += 1
    else:
      self._keys[newkey] = 1


  def sub(self, key):
    """ Decrement the count of a key in index_map.

    Existing map from `build_map()` is invalidated and future appearances of
    `key` will be ignored.
    """
    newkey = self.__access_key(key)
    if newkey in self._keys:
      self._keys[newkey] -= 1

  
  def get_count(self, key):
    """ Return the number of appearances of `key`.  """
    newkey = self.__access_key(key)
    if newkey in self._keys:
      return self._keys[newkey]
    else:
      return 0


  def build_map(self):
    '''
      Build a mapping of keys -> indices. This should only be called after all
      keys have been added to the structure.
    '''
    # Grab keys that appear at least once (skip those that have been removed)
    uniques = list(filter((lambda x: self._keys[x] > 0), self._keys.keys()))

    if self._sort:
      uniques.sort()

    # build actual mapping
    for i in range(len(uniques)):
      self._map[uniques[i]] = i+1

    self._is_mapped = True

  def is_mapped(self):
    return self._is_mapped


  def write_file(self, filename):
    '''
      Write an index map to a file. The map is inverted such that if map[X]=I,
      then X is written to the Ith line of `fout`.
    '''
    with open(filename, 'w') as fout:
      for key in sorted(self._map, key=self._map.get) :
        print(key, file=fout)


  def __getitem__(self, key):
    if not self._is_mapped:
      raise Exception('ERROR: must use `build_map()` before accessing map.')

    key = self.__access_key(key)
    if (key is None) or (key not in self._map):
      return None
    return self._map[key]

  def __len__(self):
    return len(self._map)

