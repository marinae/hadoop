import sys

INPUT_FILE = 'data/part-00000'
OFFSETS_FILE = 'data/offsets.txt'
INDEX_FILE = 'data/index'

def readInputFile(inputFile):
    keys = []
    values = []
    with open(inputFile, 'r') as f:
        lines = f.read().splitlines()
        key = ''
        encodedValue = ''
        for l in lines:
            columns = l.split('\t')
            if columns[1] != '':
                if encodedValue != '':
                    keys.append(key)
                    values.append(encodedValue)
                key = columns[0]
                encodedValue = columns[1]
            else:
                encodedValue += columns[0]
    return keys, values

def createIndex(indexFIle, values):
    offsets = []
    sizes = []
    with open(indexFIle, 'wb') as f:
        for v in values:
            offsets.append(f.tell())
            sizes.append(len(v))
            f.write(v)
    return offsets, sizes

def createDictionary(offsetsFile, keys, offsets, sizes):
    with open(offsetsFile, 'w') as f:
        for key, offset, s in zip(keys, offsets, sizes):
            f.write(str(key) + '\t' + str(offset) + '\t' + str(s) + '\n')

def main():
    keys, values = readInputFile(INPUT_FILE)
    offsets, sizes = createIndex(INDEX_FILE, values)
    createDictionary(OFFSETS_FILE, keys, offsets, sizes)

if __name__ == '__main__':
    main()
    