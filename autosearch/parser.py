from autosearch.path import PathFinder
from autosearch.utils import *

class Parser:
    def __init__(self, search, query_a, query_b):
        self.search = search

        results_a, scores_a = search(query_a)
        results_b, scores_b = search(query_b)

        result_a = parse(fetch(results_a[0]))
        result_b = parse(fetch(results_b[0]))

        finder_a = PathFinder().fromDom(result_a)
        finder_b = PathFinder().fromDom(result_b)

        paths_a = [path.shape + str(path.elements[-1].string.encode('utf-8')) for path in finder_a.paths]
        paths_b = [path.shape + str(path.elements[-1].string.encode('utf-8')) for path in finder_b.paths]

        uniq_a = [path for path in finder_a.paths if paths_a.count(path.shape + str(path.elements[-1].string.encode('utf-8'))) < 3 and paths_b.count(path.shape + str(path.elements[-1].string.encode('utf-8'))) < 3]
        uniq_b = [path for path in finder_b.paths if paths_a.count(path.shape + str(path.elements[-1].string.encode('utf-8'))) < 3 and paths_b.count(path.shape + str(path.elements[-1].string.encode('utf-8'))) < 3]

        samepaths = []

        for i, path_a in enumerate(uniq_a):
            if filter(lambda element: element.name == 'a', path_a.elements):
                continue

            tail_a = path_a.elements[-1]
            string = tail_a.string.replace('\n', '\t')

            if not testPredicate(string):
                continue

            last_j = 0
            for j, path_b in enumerate(uniq_b):
                if j < last_j:
                    continue
                if path_a.shape == path_b.shape:
                    tail_b = path_b.elements[-1]
                    if tail_a.string == tail_b.string:
                        samepaths.append(path_b)
                        last_j = j
                        break

        samepaths = PathFinder(samepaths).removeCommonRoot().paths
        self.templates = [path.shape for path in samepaths]

    def __call__(self, url):
        finder = PathFinder().fromDom(parse(fetch(url)))

        templates = self.templates
        predicates = []

        counts = list(set([templates.count(path) for path in list(set(templates))]))
        minimum = min([templates.count(path) for path in list(set(templates))])

        for template, count in sorted([(path, templates.count(path)) for path in list(set(templates))], key=lambda x: x[1], reverse=True):
            for path in finder.matchTail(template, string=True)[0]:
                string = path.elements[-1].string
                if testPredicate(string):
                    if len(counts) > 1:
                        if not count > minimum:
                            continue
                        predicates.append(template)

        objects = {}
        predicate = None
        external = []
        internal = []
        flattext = []

        willmatch = []

        for path in finder.paths:
            string = path.elements[-1].string
            shape = path.shape
            if shape not in willmatch:
                if len(filter(lambda p: path.shape.endswith(p), predicates)):
                    willmatch = list(set(willmatch + [shape]))
            if shape in willmatch and testPredicate(string):
                links = external if len(external) else internal
                texts = flattext
                if predicate and predicate not in objects and len(links + texts):
                        objects[predicate] = {
                            'links': [item for item in links if links.count(item) == 1],
                            'texts': [item for item in texts if texts.count(item) == 1],
                        }
                predicate = string.encode('utf-8')
                external = []
                internal = []
                flattext = []
            else:
                links = filter(lambda element: element.name == 'a' and 'href' in element.attrs, path.elements)
                if len(links):
                    for link in links:
                        tmp = {
                            'text': string.replace('\n', '').encode('utf-8'),
                            'href': absolutify(url, link['href']),
                        }
                        if isexternal(url, link['href']):
                            external.append(tmp)
                            break
                        else:
                            internal.append(tmp)
                            break
                if re.search('\w', string):
                    string = string.replace('\n', '')
                    flattext.append(string.encode('utf-8'))
        return objects
