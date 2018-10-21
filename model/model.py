import json
import sys
import io
import os

def process(data, file_path):
    if data['action'] == 'build':
        return build(data['path'])
    return query(data['query'], data['count'], file_path)

def build(path):
    with io.open('config.json', 'rw', encoding='utf8') as file:
        data = json.load(file)
        if data['waiting']:
            #get text terms json
            #done waiting
            #really do the building
            return 1
        #send all files for text processing
        #then start waiting the response
        text = json.dumps(data,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)
    return 0

def query(query, count, ojson):
    return 0

if not os.path.exists('config.json'):
    result = {}
    result['waiting'] = False
    result['ui'] = os.path.pardir + '\\ui\\static\\json\\action.json'
    result['text'] = os.path.pardir + '\\text\\output.json'
    with io.open('config.json', 'w', encoding='utf8') as outfile:
        text = json.dumps(result,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)

if __name__ == '__main__':
    with io.open(sys.argv[1]) as data_file:
        data = json.load(data_file)
        process(data, sys.argv[1])