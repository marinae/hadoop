#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
from itertools import groupby

initialPR = 0.15
splt = lambda line: line.strip().split('\t')

for key, group in groupby((splt(line) for line in sys.stdin), lambda line: line[0]):
    print '%s\t%.10f\t%s' % (key, initialPR, ','.join([cited for citing, cited in group]))