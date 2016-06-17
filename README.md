# autosearch.py
Automatic database searching from top page url and two keywords.

## Requirements
Minimum requirements:
- Python 2.7+
- BeautifulSoup4
- html5lib
- NumPy

### Usage
Adding a service

``` bash
# Example for adding UniProt
$ python addservice.py uniprot http://www.uniprot.org recA collagen

# Example for adding Kegg Ligand
$ python addservice.py kegg-ligand http://www.genome.jp/kegg/ligand.html glucose phsphoenolpyruvate
```

Searching a database

``` bash
# Search UniProt for Cas9
$ python autosearch.py uniprot cas9

# Output in JSON
$ python autosearch.py uniprot cas9 --json

# Match predicate
$ python autosearch.py uniprot cas9 --predicate 'enzyme regulation'
```

## How it works
autosearch.py works by first learning how to search a database, and then
learning how to parse the results. When searching a database, the learned
actions are mimicked for the input to yield results.

### Learning to search
1. Parse the top page HTML to extract every form with a text input.
2. Fetch and parse the results of submitting to each form.
3. Enumerate all HTML hierarchy paths.
4. Score paths containing query words.
5. Return the highest scoring path.
6. The form which yields the highest score is the best form.

### Actual searching
1. Search the best form.
2. Retrieve all paths with the same hierarchy as the best path.

### Learning to parse
1. Search two queries.
2. Get the top links for both queries.
3. Extract paths which are exactly the same for both results.
4. Save the paths to serve as a template.

### Actual parsing
1. Search the query.
2. Use the templates to match predicate candidates.
3. Enumerate paths between two predicate candidates.
4. Text and links are associated as objects of the previous predicate.
5.
