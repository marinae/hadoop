#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
import numpy as np
from itertools import groupby

N = len('ValueHistogram:')
splt = lambda line: line[N:].strip().split('\t', 1)

for key, group in groupby((splt(line) for line in sys.stdin), lambda line: line[0]):
    countries = [country for year, country in group]

    freq = {}
    for x in countries:
        freq[x] = freq.get(x, 0) + 1
    bin_count = freq.values()

    uniq_count = len(bin_count)             # Количество уникальных
    min_value  = np.amin(bin_count)         # Минимальное значение
    median     = np.median(bin_count)       # Медиана
    max_value  = np.amax(bin_count)         # Максимальное значение
    mean       = np.mean(bin_count)         # Среднее значение
    deviation  = np.std(bin_count)          # Стандартное отклонение

    print '%s\t%d\t%d\t%d\t%d\t%0.13f\t%0.13f' % (key, uniq_count, min_value, median, max_value, mean, deviation)