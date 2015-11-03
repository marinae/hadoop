#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
import base64
from itertools import groupby

def countDiffs(documents):
    result = []
    for i, doc in enumerate(documents):
        if i == 0:
            result.append(doc)
        else:
            result.append(doc - documents[i - 1])
    return result

def smallint2bit(x):
    bits = str(bin(x))[2:]
    return '0' * (8 - len(bits)) + bits

def int2bits(x):
    bits = []
    if x == 0:
        bits.append('00000000')
    while x > 0:
        bits.append(smallint2bit(x % 128))
        x = x / 128
    bits[0] = '1' + bits[0][1:]
    return ''.join(bits[::-1])

class BitstreamWriter:
    def __init__(self):
        self.nbits = 0
        self.curbyte = 0
        self.vbytes = []

    def add(self, x):
        self.curbyte |= x << (8 - 1 - (self.nbits % 8))
        self.nbits += 1

        if self.nbits % 8 == 0:
            self.vbytes.append(chr(self.curbyte))
            self.curbyte = 0

    def getbytes(self):
        if self.nbits & 7 == 0:
            return ''.join(self.vbytes)

        return ''.join(self.vbytes) + chr(self.curbyte)

class Encoder:
    def __init__(self, mode):
        if mode == 'VarByte' or mode == 'Simple9':
            self.mode = mode
        else:
            raise ValueError('Invalid mode specified in command line')

    def encode(self, diffs):
        if self.mode == 'VarByte':
            return self.encodeVarByte(diffs)
        else:
            return self.encodeSimple9(diffs)

    def encodeVarByte(self, diffs):
        bits = ''.join([int2bits(x) for x in diffs])
        bw = BitstreamWriter()
        for i in bits:
            bw.add(int(i))
        return bw.getbytes()

    def encodeSimple9(self, diffs):
        result = []
        return result

encoder = Encoder(sys.argv[1])

splt = lambda line: line.strip().split('\t')

for key, group in groupby((splt(line) for line in sys.stdin), lambda line: line[0]):
    documents = sorted([int(document) for word, document in group])
    diffs = countDiffs(documents)
    print '%s\t%s' % (key, base64.encodestring(encoder.encode(diffs)).strip())
