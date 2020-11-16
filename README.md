# KayakCompress

Run the compression with: $ python3 compress.py <input_coords.csv> <epsilon> <optional -flag>
use -test with Running.csv to get a before/after plot outputted in a .html file on a map.
use -log to print arrays in the console

The input should be in a .csv file with columns consisting of a timestamp, latitude and longitude, in that order. The timestamps are unused at the moment.

The output is placed in compressedCoords.csv, containing latitude and longitude.
