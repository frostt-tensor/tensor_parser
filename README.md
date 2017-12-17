Tensor Parser
=============

[![Build Status](https://travis-ci.org/frostt-tensor/tensor_parser.svg?branch=master)](https://travis-ci.org/frostt-tensor/tensor_parser)

A package for constructing sparse tensors from CSV-like data sources.


## Mode Types


## Handling Duplicates
By default, duplicate non-zero values are removed and their values are summed.
This behavior can be changed with `--merge=<func>`, which takes one of the
following options:

  * none (do not remove duplicate non-zeros)
  * sum
  * min
  * max
  * avg
  * count (use the number of duplicates)

Note that merging duplicates requires the tensor to be sorted. A disk-based
sort is provided by the `csvsorter` library.


## Example 1
Suppose you have the following CSV file:

    $ zcat traffic.csv.gz
    Date Of Stop,Time Of Stop,Latitude,Longitude,Description
    01/01/2013,02:23:00,39.0584153167,-77.0480714833,DUI
    01/01/2013,01:45:00,38.9907737666667,-77.1545810833333,SPEEDING
    01/01/2013,05:15:00,39.288735,-77.20448,DWI
    ....

We want to keep the dates, hour of violation, lower-case description, and round
the geolocations to three decimal places:

    $ ./scripts/build_tensor.py traffic.csv.gz traffic.tns \
        -f "date of stop" --type="date of stop",date \
        -f "time of stop" --type="time of stop",hour \
        -f latitude -f longitude --type=latitude,longitude,roundf-3 \
        -f description --type=description,"lambda x : x.lower()"



## Testing
This project uses the builtin `unittest` library provided by Python. You can
run all unit tests via:

    $ python3 -m unittest

