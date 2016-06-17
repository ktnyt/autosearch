# -*- coding: utf-8 -*-
import argparse
import cPickle as pickle

import json

import autosearch

def dump(objects, predicate, join_text, text_only, link_only):
    keys = objects.keys()

    if predicate:
        match = [key for key in keys if predicate.lower() == key.lower()]
        keys = match

    for key in sorted(keys):
        print key
        if not text_only:
            for link in objects[key]['links']:
                print '- Link:', link['href'], link['text']
        if not link_only:
            if join_text:
                print ' '.join(objects[key]['texts'])
            else:
                for text in objects[key]['texts']:
                    print '- Text:', text

def main():
    parser = argparse.ArgumentParser(description='Add service to autosearcher')

    parser.add_argument('service', type=str, help='Name of service to setup')
    parser.add_argument('query', type=str, help='Search query 1')
    parser.add_argument('--pickle', type=str, default='services.pkl', help='Pickle file')

    parser.add_argument('--predicate', default=None, help='Predicate to extract')
    parser.add_argument('--join_text', default=False, help='Join text with space', action='store_true')
    parser.add_argument('--text_only', default=False, help='Only report texts', action='store_true')
    parser.add_argument('--link_only', default=False, help='Only report links', action='store_true')

    parser.add_argument('--json', default=False, help='Output results in json', action='store_true')

    args = parser.parse_args()

    with open(args.pickle, 'r') as f:
        services = pickle.load(f)

    if args.service not in services:
        print 'Service "{}" not availablein {}: try adding one.'.format(args.service, args.pickle)

    objects, results = services[args.service](args.query)

    if args.json:
        print json.dumps(objects, sort_keys=True).decode('unicode-escape').encode('utf8')
        return

    for obj in objects:
        dump(obj, args.predicate, args.join_text, args.text_only, args.link_only)


if __name__ == '__main__':
    main()
