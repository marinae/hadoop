#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
from itertools import groupby

N = len('ValueHistogram:')
splt = lambda line: line[N:].strip().split('\t', 1)

for key, group in groupby((splt(line) for line in sys.stdin), lambda line: line[0]):
    countries = [country for year, country in group]

    freq = {}
    for x in countries:
        freq[x] = freq.get(x, 0) + 1
    bin_count = freq.values()

    uniq_count = len(bin_count)  # Количество уникальных

    sumForMean = 0
    for i in bin_count:
        sumForMean += i
    mean = sumForMean / float(uniq_count)  # Среднее значение

    sumForDev = 0
    for i in bin_count:
        sumForDev += (i - mean)**2
    deviation = (sumForDev / float(uniq_count))**(0.5)  # Стандартное отклонение

    median = sorted(bin_count)[uniq_count / 2]  # Медиана

    min_value  = min(bin_count)             # Минимальное значение
    max_value  = max(bin_count)             # Максимальное значение    

    print '%s\t%d\t%d\t%d\t%d\t%0.13f\t%0.13f' % (key, uniq_count, min_value, median, max_value, mean, deviation)