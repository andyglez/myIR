import json
import sys
import io
import os

def printJson(file, data):
    with io.open(file, 'w', encoding='utf8') as output:
        text = json.dumps(data,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        output.write(text)

def readJson(file):
    with io.open(file, 'r', encoding='utf8') as file:
        return json.load(file)

def process(data, file_path):
    if data['action'] == 'build':
        return build(data['path'])
    return query(data['query'], data['count'], file_path)

def build(path):
    with io.open('config.json', 'rw', encoding='utf8') as file:
        data = json.load(file)
        if data['waiting']:
            #get text terms json
            terms = readJson(data['text'])['terms']
            #done waiting
            data['waiting'] = False
            #really do the building
            return index(terms)
        
        #send all files for text processing
        plain = ''
        for f in os.scandir(path):
            if os.path.isfile(f):
                with io.open(path + f, 'r', encoding='utf8') as in_path:
                    #still must check for PDFs
                    t = in_path.read()
                    plain = plain + t
        data['ready'] = False
        data['waiting'] = True
        result = {}
        result['action'] = 'process'
        result['data'] = plain
        printJson(data['text'], result)
        #then start waiting the response
        text = json.dumps(data,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)
    return 0

def index(terms):
    return 0

def query(query, count, ojson):
    return 0

if not os.path.exists('config.json'):
    result = {}
    result['waiting'] = False
    result['ready'] = True
    result['ui'] = os.path.pardir + '\\ui\\static\\json\\action.json'
    result['text'] = os.path.pardir + '\\text\\text.json'
    with io.open('config.json', 'w', encoding='utf8') as outfile:
        text = json.dumps(result,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)

if __name__ == '__main__':
    with io.open(sys.argv[1]) as data_file:
        data = json.load(data_file)
        process(data, sys.argv[1])