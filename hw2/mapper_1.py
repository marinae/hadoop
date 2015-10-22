#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

for line in sys.stdin:
    fields = line.strip().split('\t')
    citings = fields[2].split(',')

    print '%s' % line.strip()

    for x in citings:
        print '%s\t%0.10f\t#' % (x, float(fields[1]) / len(citings))