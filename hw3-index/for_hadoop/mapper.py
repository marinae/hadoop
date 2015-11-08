#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import base64
import zlib
import HTMLParser
from zipimport import zipimporter

bs4_importer = zipimporter('bs4.zip')
bs4 = bs4_importer.load_module('bs4')

def stripScripts(html):

    cleanHtml = re.sub('<script([\s\S]+?)</script>', '', html)
    cleanHtml = re.sub('<style([\s\S]+?)</style>', '', cleanHtml)
    return cleanHtml

def getTerms(compressed):

    try:
        html = zlib.decompress(base64.decodestring(compressed))
        soup = bs4.BeautifulSoup(stripScripts(html), 'html.parser')
        text = ' '.join(soup.get_text().lower().split())
        cleanText = re.sub(u'[^a-zа-яё0-9]+', ' ', text)
        return set(cleanText.split())

    except HTMLParser.HTMLParseError:
        return set()

for line in sys.stdin:

    fields = line.strip().split('\t')
    terms = getTerms(fields[1])

    for t in terms:
        print '%s\t%s' % (t.encode('utf-8'), fields[0])
        