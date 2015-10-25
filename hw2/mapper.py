#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

for line in sys.stdin:
    fields = line.strip().split('\t')

    if len(fields) == 3:
        print '%s' % line.strip()

        citings = fields[2].split(',')
        for x in citings:
            print '%s\t%0.10f\t' % (x, float(fields[1]) / len(citings))