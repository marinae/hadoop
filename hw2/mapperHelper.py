#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

for line in sys.stdin:
    if line.startswith('"'):
        continue
    fields = line.strip().split(',')
    print '%s\t%s' % (fields[0], fields[1])