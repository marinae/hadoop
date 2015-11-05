import math
import base64

#   bits/number numbers mode
schemas = [[1,  28, '0000'],
           [2,  14, '0001'],
           [3,  9,  '0010'],
           [4,  7,  '0011'],
           [5,  5,  '0100'],
           [7,  4,  '0101'],
           [9,  3,  '0110'],
           [14, 2,  '0111'],
           [28, 1,  '1000']]

def countDiffs(documents):
    result = []
    for i, doc in enumerate(documents):
        if i == 0:
            result.append(doc)
        else:
            result.append(doc - documents[i - 1])
    return result

def sumDiffs(diffs):
    result = []
    for i, d in enumerate(diffs):
        if i == 0:
            result.append(d)
        else:
            result.append(d + result[i - 1])
    return result

def smallint2bit(x, length=8):
    bits = str(bin(x))[2:]
    return '0' * (length - len(bits)) + bits

def int2bits(x):
    bits = []
    if x == 0:
        bits.append('00000000')
    while x > 0:
        bits.append(smallint2bit(x % 128))
        x = x / 128
    bits[0] = '1' + bits[0][1:]
    return ''.join(bits[::-1])

def bitSize(x):
    return int(math.floor(math.log(x, 2) + 1) if x != 0 else 1)

def getScheme(sizes):
    N = len(sizes)
    for s in schemas[:-1]:
        if N < s[1]:
            continue
        flag = True
        sumSize = 0
        for i in xrange(s[1]):
            sumSize += sizes[i]
            if sumSize > 28 or sizes[i] > s[0]:
                flag = False
                break
        if flag:
            return s
    return schemas[-1]

def encodePack(scheme, diffs, length):
    bits = scheme
    for d in diffs:
        bits += smallint2bit(d, length)
    return bits

def decodePack(scheme, bits):
    s = schemas[int(scheme, 2)]
    diffs = []
    for i in xrange(s[1]):
        diffs.append(int(bits[:s[0]], 2))
        bits = bits[s[0]:]
    return diffs

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

class BitstreamReader:
    def __init__(self, blob):
        self.blob = blob
        self.pos  = 0

    def get(self):
        ibyte = self.pos / 8
        ibit  = self.pos & 7

        self.pos += 1
        return (ord(self.blob[ibyte]) & (1 << (7 - ibit))) >> (7 - ibit)

    def finished(self):
        return self.pos >= len(self.blob) * 8

class Encoder:
    def __init__(self, mode):
        if mode == 'VarByte' or mode == 'Simple9':
            self.mode = mode
        else:
            raise ValueError('Invalid mode specified in command line')

    def encodeVarByte(self, diffs):
        return ''.join([int2bits(x) for x in diffs])

    def decodeVarByte(self, bits):
        diffs = []
        while len(bits) > 0:
            cur = 0
            while bits[0] == '0':
                cur += int(bits[:8], 2)
                cur *= 128
                bits = bits[8:]
            byte = '0' + bits[1:8]
            cur += int(byte, 2)
            bits = bits[8:]
            diffs.append(cur)
        return diffs

    def encodeSimple9(self, diffs):
        sizes = [bitSize(i) for i in diffs]
        bits = ''
        while len(diffs) > 0:
            s = getScheme(sizes)
            pack = encodePack(s[2], diffs[:s[1]], s[0])
            bits += pack + '0' * (32 - len(pack))
            diffs = diffs[s[1]:]
            sizes = sizes[s[1]:]
        return bits

    def decodeSimple9(self, bits):
        diffs = []
        while len(bits) > 0:
            diffs.extend(decodePack(bits[:4], bits[4:32]))
            bits = bits[32:]
        return diffs

    def encode(self, docs):
        diffs = countDiffs(sorted(docs))
        if self.mode == 'VarByte':
            bits = self.encodeVarByte(diffs)
        else:
            bits = self.encodeSimple9(diffs)
        bw = BitstreamWriter()
        for i in bits:
            bw.add(int(i))
        return base64.encodestring(bw.getbytes())[:-1]

    def decode(self, blob):
        bits = ''
        br = BitstreamReader(base64.decodestring(blob))
        while not br.finished():
            bits += str(br.get())
        if self.mode == 'VarByte':
            diffs = self.decodeVarByte(bits)
        else:
            diffs = self.decodeSimple9(bits)
        return sumDiffs(diffs)
