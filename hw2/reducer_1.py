#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
from itertools import groupby

initialPR = 0.15
splt = lambda line: line.strip().split('\t')

for key, group in groupby((splt(line) for line in sys.stdin), lambda line: line[0]):
    sumRank = 0.0
    cited = '#'

    patents = [x for x in group]

    for p in patents:
        if p[2] == '#':
            sumRank += float(p[1])
        else:
            cited = p[2]

    print '%s\t%.10f\t%s' % (key, sumRank, cited)