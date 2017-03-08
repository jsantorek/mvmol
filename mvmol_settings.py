#!/usr/bin/python

# input file:
# 1. No header, must start with 1st test
i_file = 'input/input.txt'
scaling_factors = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
# [0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15]
# Headers to be written in all generated output files
o_header1 = 'BASIS\n'
o_header2 = 'aug-cc-pVDZ\n'
o_header3 = '\n'
o_header4 = '\n'
# Path and name for all output files
o_prefix = 'output/'
