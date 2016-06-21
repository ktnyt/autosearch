from autosearch.form import Form
from autosearch.path import Path, PathFinder
from autosearch.utils import *

class Searcher(object):
    def __init__(self, url, query):
        self.url = url

        top = addScore(parse(fetch(url)), query)

        forms = []
        paths = []
        scores = []

        # Find forms with text inputs
        for form in top.find_all('form'):
            if 'action' not in form.attrs:
                continue
            form['action'] = absolutify(url, form['action'])
            for input in form.find_all('input'):
                attrs = input.attrs
                if 'type' not in attrs or attrs['type'] in ['text', 'search']:
                    forms.append(Form(form))

        if not len(forms):
            return

        # Try each form
        for form in forms:
                result = form(query)
                finder = PathFinder().fromDom(result, tag='a', attr='href')
                path, score = finder.bestPath()
                paths.append(path)
                scores.append(score)

        # Find best form
        i = argmax(scores)

        form, path = forms[i], paths[i]

        self.form = form
        self.path = path.stringify()

    def __call__(self, query):
        form = self.form
        path = self.path
        result = form(query)
        finder = PathFinder().fromDom(result, tag='a', attr='href')
        matches, scores = finder.matchPath(path, string=True)
        return [absolutify(form.action, match.elements[-1]['href']) for match in matches], scores
