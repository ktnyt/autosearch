from bs4.element import Tag, NavigableString

from autosearch.utils import *

class Path(object):
    def __init__(self, elements):
        self.elements = elements
        self.score = 0
        self.shape = self.stringify()
        for element in elements:
            if hasattr(element, 'attrs'):
                if 'score' in element.attrs:
                    self.score += element['score']

    def stringify(self, classes=False):
        strings = []
        for element in self.elements:
            name = element.name
            if name is None:
                name = 'text'
            if name in ['td']:
                index = 0
                if element.parent:
                    for sibling in element.parent.children:
                        if sibling == element:
                            name += str(index)
                            break
                        if sibling.name == name:
                            index += 1
            if classes:
                if hasattr(element, 'attrs'):
                    if 'class' in element.attrs:
                        name += ' ' + ' '.join(element['class'])
            strings.append('<{}>'.format(name))
        return ''.join(strings)

class PathFinder(object):
    def __init__(self, paths=[]):
        self.paths = paths

    def fromDom(self, element, tag=None, attr=None):
        self.paths = []

        def subpath(element, path=[]):
            if tag is None:
                if not hasattr(element, 'children'):
                    self.paths.append(Path(path + [element]))
            if isinstance(element, Tag):
                if element.name == tag:
                    if attr is None or attr in element.attrs:
                        self.paths.append(Path(path + [element]))
            if hasattr(element, 'children'):
                for child in element.children:
                    subpath(child, path=path + [element])

        subpath(element)
        return self

    def bestPath(self):
        tuples = []
        for path in self.paths:
            tuples.append((path, path.score))
        paths, scores = zip(*tuples)
        i = argmax(scores)
        return paths[i], scores[i]

    def matchPath(self, query, string=False):
        if not string:
            query = query.stringify()
        matches = []
        scores = []
        for path in self.paths:
            if path.stringify() == query:
                matches.append(path)
                scores.append(path.score)
        return matches, scores

    def matchHead(self, query, string=False):
        if not string:
            query = query.stringify()
        matches = []
        scores = []
        for path in self.paths:
            if path.stringify().startswith(query):
                matches.append(path)
                scores.append(path.score)
        return matches, scores

    def matchTail(self, query, string=False):
        if not string:
            query = query.stringify()
        matches = []
        scores = []
        for path in self.paths:
            if path.stringify().endswith(query) or query.endswith(path.stringify()):
                matches.append(path)
                scores.append(path.score)
        return matches, scores

    def removeCommonRoot(self):
        lens = [len(path.elements) for path in self.paths]
        shortest = self.paths[argmax(lens)]
        trimmed = []

        for depth in range(len(shortest.elements)-1):
            path = Path(shortest.elements[0:depth])
            matches, scores = self.matchHead(path)
            if len(matches) != len(self.paths):
                break
            trimmed = [Path(path.elements[depth:]) for path in self.paths]

        self.paths = trimmed
        return self
