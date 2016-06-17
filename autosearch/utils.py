import re
import numpy as np
import urllib2
from urlparse import urlparse

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

def argmax(array):
    return np.argmax(np.array(array))

def parse(contents):
    contents = contents.replace('&lt;', '<').replace('&gt;', '>')
    return BeautifulSoup(contents, 'html5lib').html

def fetch(url):
    response = urllib2.urlopen(url)
    return response.read()

def getScore(element, query):
    value = 0
    if isinstance(element, NavigableString):
        if re.search(query, element.string, re.IGNORECASE):
            value += 1
    if isinstance(element, Tag):
        for child in element.children:
            value += getScore(child, query)
    return value

def addScore(element, query, depth=0):
    if isinstance(element, Tag):
        element['score'] = getScore(element, query) * depth
        for child in element.children:
            addScore(child, query, depth=depth+1)
    return element

def absolutify(url, href):
    if href == '/':
        p = urlparse('')
    elif len(href) and href[0] == '/' and href[1] != '/':
        href = href[1:]
    o = urlparse(url)
    p = urlparse(href)
    if not len(p.scheme):
        p = p._replace(scheme=o.scheme)
    if not len(p.netloc):
        p = p._replace(netloc=o.netloc)
    return p.geturl()

def isexternal(url, href):
    o = urlparse(url)
    p = urlparse(href)
    return len(p.netloc) and o.netloc != p.netloc

def testPredicate(predicate):
    if len(predicate) < 2 or len(predicate.split(' ')) > 5:
        return False
    if not re.search('[A-Za-z]', predicate):
        return False
    if re.search('[\+;\'"]', predicate):
        return False
    if not re.search('^\w', predicate):
        return False
    return True
