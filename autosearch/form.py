import urllib
import urllib2

from autosearch.utils import *

class Form(object):
    def __init__(self, form):
        self.query = ''
        self.action = form['action']
        self.params = {}

        for input in form.find_all('input'):
            attrs = input.attrs
            if not 'name' in attrs:
                continue
            name = attrs['name']
            if len(name) > 20:
                continue
            if not 'value' in attrs:
                value = None
            else:
                value = attrs['value']
            self.params[name] = value

            if 'type' not in attrs or attrs['type'] in ['text', 'search']:
                if value is None or not len(value):
                    self.query = name

        for select in form.find_all('select'):
            attrs = select.attrs
            if not 'name' in attrs:
                continue
            name = select['name']
            for option in select.find_all('option'):
                attrs = option.attrs
                if not 'selected' in attrs:
                    continue
                if not 'value' in attrs:
                    continue
                value = attrs['value']
                if value is not None:
                    self.params[name] = value

    def __call__(self, query):
        values = self.params
        values[self.query] = query
        data = urllib.urlencode(values)
        url = '{}?{}'.format(self.action, data)
        return addScore(parse(fetch(url)), query)
