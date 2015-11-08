import sys
from encoder import Encoder

URLS_FILE = 'data/urls.txt'
OFFSETS_FILE = 'data/offsets.txt'
INDEX_FILE = 'data/index'

def parseArgs(query):
    ors = query.split('OR')
    ands = [x.split('AND') for x in ors]
    words = ands
    for i, w in enumerate(words):
        for j, x in enumerate(w):
            words[i][j] = [y.strip() for y in words[i][j].split('NOT')]
        words[i] = sorted(words[i], key=len)
    return words

def getUrls(f, e, wordDict, word):
    if word not in wordDict:
        return []
    entry = wordDict[word]
    offset = entry[0]
    bytelen = entry[1]
    f.seek(int(offset))
    blob = f.read(int(bytelen))
    urls = e.decode(blob)
    return urls

def performAnd(prev, cur):
    result = []
    i = 0
    j = 0
    while i < len(prev) and j < len(cur):
        while i < len(prev) and prev[i] < cur[j]:
            i += 1
        while i < len(prev) and j < len(cur) and cur[j] < prev[i]:
            j += 1
        if i < len(prev) and j < len(cur) and prev[i] == cur[j]:
            result.append(prev[i])
            i += 1
            j += 1
    return result

def performAndNot(prev, cur):
    result = []
    i = 0
    j = 0
    while i < len(prev) and j < len(cur):
        while i < len(prev) and prev[i] < cur[j]:
            result.append(prev[i])
            i += 1
        while i < len(prev) and j < len(cur) and cur[j] < prev[i]:
            j += 1
        if i < len(prev) and j < len(cur) and prev[i] == cur[j]:
            i += 1
            j += 1
    while i < len(prev):
        result.append(prev[i])
        i += 1
    return result

def performOr(prev, cur):
    result = []
    i = 0
    j = 0
    while i < len(prev) and j < len(cur):
        while i < len(prev) and prev[i] < cur[j]:
            result.append(prev[i])
            i += 1
        while i < len(prev) and j < len(cur) and cur[j] < prev[i]:
            result.append(cur[j])
            j += 1
        if i < len(prev) and j < len(cur) and prev[i] == cur[j]:
            result.append(prev[i])
            i += 1
            j += 1
    while i < len(prev):
        result.append(prev[i])
        i += 1
    while j < len(cur):
        result.append(cur[j])
        j += 1
    return result

def queryUrls(e, wordDict, query):
    words = parseArgs(query)
    result = []

    with open(INDEX_FILE, 'r') as f:    
        for ands in words:
            resultOfAnd = []
            for i, w in enumerate(ands):
                cur = getUrls(f, e, wordDict, w[-1])
                if i == 0:
                    resultOfAnd = cur
                elif len(w) == 1:
                    resultOfAnd = performAnd(resultOfAnd, cur)
                else:
                    resultOfAnd = performAndNot(resultOfAnd, cur)
            result = performOr(result, resultOfAnd)

    return result

def main(mode):
    with open(OFFSETS_FILE, 'r') as f:
        lines = f.read().splitlines()
        columns = [l.split('\t') for l in lines]
        wordDict = dict([(c[0], [c[1], c[2]]) for c in columns])

    with open(URLS_FILE, 'r') as f:
        lines = f.read().splitlines()
        allUrls = [l.split('\t')[1] for l in lines]

    while True:
        try:
            print '>> ',
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            break

        if not line:
            break
        elif line == '\n':
            print '\rNothing found'
        else:
            e = Encoder(mode)
            urls = queryUrls(e, wordDict, line)
            for i, u in enumerate(urls):
                print '\r%d. %s' % (i + 1, allUrls[u])

if __name__ == '__main__':
    main(sys.argv[1])