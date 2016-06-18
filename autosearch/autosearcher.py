from autosearch.searcher import Searcher
from autosearch.parser import Parser

class Autosearcher(object):
    def __init__(self, url, query_a, query_b):
        self.search = Searcher(url, query_a)
        self.parse = Parser(self.search, query_a, query_b)

    def __call__(self, query, n=1):
        results, scores = self.search(query)
        n = min([n, len(results)])
        objects = [self.parse(result) for result in results[0:n]]
        return objects, results
