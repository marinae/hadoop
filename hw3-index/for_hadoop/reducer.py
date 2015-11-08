#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
from itertools import groupby
from zipimport import zipimporter

encoder_importer = zipimporter('encoder.zip')
encoder = encoder_importer.load_module('encoder')

e = encoder.Encoder(sys.argv[1])
splt = lambda line: line.strip().split('\t')

for key, group in groupby((splt(line) for line in sys.stdin), lambda line: line[0]):
    documents = [int(document) for word, document in group]
    print '%s\t%s' % (key, e.encode(documents))
