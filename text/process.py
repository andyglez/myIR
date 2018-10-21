import sys
import json

def process(file):
    terms = clean(file)
    result = {}
    result['terms'] = terms
    return result

def clean(file):
    return 0


if __name__ == '__main__':
    for json in sys.argv[1:]:
        process(json)