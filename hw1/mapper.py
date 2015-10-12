#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

index1 = int(sys.argv[1])
index2 = int(sys.argv[2])

for line in sys.stdin:
    if line.startswith('"'):
        continue
    fields = line.split(',')
    print 'ValueHistogram:%s\t%s' % (fields[index1], fields[index2])