#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

freeRank = 0.0

for line in sys.stdin:
    fields = line.strip().split('\t')

    citing = 0

    if fields[2] != '#':
        citing = fields[0]

    print '%s\t%s\t%s' % (citing, fields[1], fields[2])