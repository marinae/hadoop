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
        bits = ''.join([int2bits(x) for x in diffs])
        print bits
        bw = BitstreamWriter()
        for i in bits:
            bw.add(int(i))
        return bw.getbytes()

    def decodeVarByte(self, blob):
        bits = ''
        br = BitstreamReader(blob)
        while not br.finished():
            bits += str(br.get())
        print bits
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
        print diffs
        return diffs

    def encodeSimple9(self, diffs):
        return 'blob'

    def decodeSimple9(self, blob):
        return []

    def encode(self, docs):
        diffs = countDiffs(sorted(docs))
        print diffs
        if self.mode == 'VarByte':
            return self.encodeVarByte(diffs)
        else:
            return self.encodeSimple9(diffs)

    def decode(self, blob):
        if self.mode == 'VarByte':
            diffs = self.decodeVarByte(blob)
        else:
            diffs = self.decodeSimple9(blob)
        return sumDiffs(diffs)
