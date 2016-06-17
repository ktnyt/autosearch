import argparse
import cPickle as pickle

import autosearch

def addservice(name, url, query1, query2, filename):
    try:
        with open(filename, 'r') as f:
            services = pickle.load(f)
    except:
        services = {}

    services[args.name] = autosearch.Autosearcher(args.url, args.query1, args.query2)

    with open(filename, 'w') as f:
        pickle.dump(services, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add service to autosearcher')
    parser.add_argument('name', type=str, help='Name of service to setup')
    parser.add_argument('url', type=str, help='Url to top page of service')
    parser.add_argument('query1', type=str, help='Search query 1')
    parser.add_argument('query2', type=str, help='Search query 2')
    parser.add_argument('--pickle', type=str, default='services.pkl', help='Pickle file')
    args = parser.parse_args()

    print 'Adding service "{}" ({}) with queries "{}" and "{}" to "{}"'.format(args.name, args.url, args.query1, args.query2, args.pickle)
    addservice(args.name, args.url, args.query1, args.query2, args.pickle)
