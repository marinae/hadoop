#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
from itertools import groupby

NODE_COUNT = 2089345
ALPHA = 0.15
RANDOM_JUMP = ALPHA / NODE_COUNT

splt = lambda line: line.strip().split('\t')
freeRank = 0.0

for key, group in groupby((splt(line) for line in sys.stdin), lambda line: line[0]):

    patents = [x for x in group]

    for p in patents:
        if p[0] == '0':
            freeRank += float(p[1])
        else:
            fullRank = RANDOM_JUMP + (1 - ALPHA) * (freeRank / NODE_COUNT + float(p[1]))
            print '%s\t%.10f\t%s' % (key, fullRank, p[2])