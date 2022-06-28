import urllib.parse
import sys

with open(sys.argv[1], 'r') as f:
    for q in f:
        print('/select?q=text:' + urllib.parse.quote(q))
