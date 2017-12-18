Tensor Parser
=============

[![Build Status](https://travis-ci.org/frostt-tensor/tensor_parser.svg?branch=master)](https://travis-ci.org/frostt-tensor/tensor_parser)

A package for constructing sparse tensors from CSV-like data sources. This
package constructs mappings from columns in the CSV file(s) to contiguous
indices in the tensor and merges duplicate non-zeros (i.e., duplicate rows).


## Requirements
`tensor_parser` is written in Python3. Its dependencies are:
  * `python` >= 3.4
  * `python-dateutil`
  * `csvsorter`

To install external dependencies, you can simply use `pip`:

    $ pip install -r requirements.txt

To run, use the entry point:

    $ ./scripts/build_tensor.py --help


## CSV Files
We support CSV files stored in text, compressed gzip (`.gz`), or compressed
bzip2 (`.bz2`) formats.

By default, we attempt to auto-detect the header and delimiter of the CSV file
via Python's supplied CSV parsing library. The `--query` option will query the
detected CSV metadata and print to `STDOUT`:

    $ ./build/build_tensor.py traffic.csv.gz out.tns --query
    Found delimiter: ","
    Found fields:
    ['Date Of Stop', 'Time Of Stop', 'Latitude', 'Longitude', 'Description']

Note that `out.tns` is not touched when querying a CSV file, though it is
required as a positional argument.

Any numer of CSV files can be provided for output, so long as the fields used
to construct the sparse tensor are found in each file.

If no header is detected, a default of `["1", "2", ...]` is used.

If you wish to use something other than the detected delimiter or field names,
they can be modified with `--field-sep=` and `--has-header=<yes,no>`.


## Tensor Files
Two types of files are created:
  * Sparse tensor (`.tns`): the actual tensor data. Each line is a list of
    indices and a value. For example, `1 1 1 1.38` would be one non-zero in a
    third-order tensor.
  * Mode mappings (`.map`): map the tensor indices to the original values in
    the source data. Line `i` is the source data that was mapped to index `i`
    in the tensor.
For more information on file formats, see
[FROSTT](http://frostt.io/tensors/file-formats.html).


## Tensor Construction
### Mode selection
Columns of the CSV file (referred to as "fields") are selected using the
`--field=` flag (abbreviated `-f`). If the CSV file has a header, the supplied
parameter must match a field in the header (but is **not** case sensitive).
Otherwise, the columns are referenced by number and one-indexed. If the field
has spaces in the name, simply enclose it in quotes: `--field="time of day"`.


### Tensor values
A field of the CSV file can be selected to be used as the values of the tensor
using the `--vals=` flag. If no field is selected to use as the tensor values,
`1` is used and the resulting tensor is one of count data.


## Mode Types
A critical step when constructing a sparse tensor is to select the datatype of
the CSV columns. When the CSV is parsed, the fields are read and sorted as
strings. Thus, values with the same string representation are mapped to the
same index in the tensor mode. In practice, however, columns often should be
treated as integers, floats, dates, or other types.

In addition to affecting the ordering of the resulting indices, the type of a
column affects the mapping of CSV entries to unique indices. For example, one
may wish to round floats such that `1.38` and `1.38111` map to the same index,
or to map dates `Aug 20` and `August 20` to the same index.

We provide several types which can be specified with the `--type=` flag:
  * `str` => String (default)
  * `int` => Integer
  * `float` => Floating-point number
  * `roundf-X` => Floating-point numbers rounded to `X` decimal places
  * `date` => A `datetime` object that encodes year, month, day, hour,
    minute, second, and millisecond
  * `year` => A year (integer extracted from `date`)
  * `month` => A month (integer in range [0,11] extracted from `date`)
  * `day` => A day (integer in range [0,30] extracted from `date`)
  * `hour` => A hour (integer in range [0,23] extracted from `date`)
  * `min` => A min (integer in range [0,60] extracted from `date`)
  * `sec` => A sec (integer in range [0,60] extracted from `date`)

Smart date matching is provided by the
[dateutil](https://pypi.python.org/pypi/python-dateutil) package. For example,
`"Aug 20"` and `"08/20/92"` will map to the same index if the type is either
`month` or `day`. However, the package maps to the current year if none is
specified, and thus they will map to different indices if the type is `year`.

You can specify multiple fields in the same `--type` instance. For example:
`--type=userid,itemid,int` would treat the fields `userid` and `itemid` both
as integers.


### Advanced mode types
A "type" in our context is any object which supports:
  * construction: `type("X")` should return some representation of "X"
  * comparison: `__le__()` is required to sort indices. If no comparison is
    possible, be sure to disable sorting of the mode with `--no-sort`
  * printing: `__str__()` is required to construct `.map` files
The specification of a type is as simple as providing a function which maps a
string to some object. Conveniently, most builtin types already support this
interface via their constructors. Functions such as `int()` and `float()`
work well.

Many types can be specified with a short anonymous function. If the specified
type is not found in the list of builtin types (above), then it is treated
as source code and specifies a custom type. For example,

    --type=cost,"lambda x : float(x) * 1.06"

may be a method of scaling all costs by 6% to account for sales tax. Note that
all type functions take a single parameter which will be an `str` object.



## Handling Duplicates
By default, duplicate non-zero values are removed and their values are summed.
This behavior can be changed with `--merge=`, which takes one of the following
options:

  * `none` (do not remove duplicate non-zeros)
  * `sum`
  * `min`
  * `max`
  * `avg`
  * `count` (use the number of duplicates)

Note that merging duplicates requires the tensor to be sorted. A disk-based
sort is provided by the [csvsorter](https://github.com/dionysio/csvsorter)
library.


## Example
Suppose you have the following CSV file:

    $ zcat traffic.csv.gz
    Date Of Stop,Time Of Stop,Latitude,Longitude,Description
    01/01/2013,02:23:00,39.0584153167,-77.0480714833,DUI
    01/01/2013,01:45:00,38.9907737666667,-77.1545810833333,SPEEDING
    01/01/2013,05:15:00,39.288735,-77.20448,DWI

We want to keep the dates, hour of violation, lower-case description, and round
the geolocations to three decimal places:

    $ ./scripts/build_tensor.py traffic.csv.gz traffic.tns \
        -f "date of stop" --type="date of stop",date \
        -f "time of stop" --type="time of stop",hour \
        -f latitude -f longitude --type=latitude,longitude,roundf-3 \
        -f description --type=description,"lambda x : x.lower()"

The resulting tensor is built:

    $ cat mode-1-dateofstop.map
    2013-01-01 00:00:00

    $ cat mode-2-timeofstop.map
    1
    2
    5

    $ cat mode-3-latitude.map
    38.991
    39.058
    39.289

    $ cat mode-4-longitude.map
    -77.204
    -77.155
    -77.048

    $ cat mode-5-description.map
    dui
    dwi
    speeding

    $ cat traffic.tns
    1 1 1 2 3 1
    1 2 2 3 1 1
    1 3 3 1 2 1



## Testing
This project uses the builtin `unittest` library provided by Python. You can
run all unit tests via:

    $ python3 -m unittest

