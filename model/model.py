import json
import io
import os
from time import time

def process(data, state, output):
    if state == 1:
        return get_terms(data, output)
    if state == 2:
        return analise_model(data['terms'], output)
    return report(data, output)

def get_terms(data, output):
    if data['action'] == 'build':
        globals()['is_query'] = False
        globals()['path'] = data['path']
        return scan(data['path'], output)
    globals()['query_count'] = data['count']
    globals()['is_query'] = True
    return terms(data['query'], output)

def scan(path, output):
    try:
        plain = ''
        for file in os.scandir(path):#[x for x in os.scandir(path) if os.path.isfile(x)]:
            with io.open(file, 'r', encoding='utf8') as text:
                for line in text.readlines():
                    plain = plain + line
        return terms(plain, output)
    except:
        return False
    

def terms(plain, output):
    result = {}
    result['action'] = 'process'
    result['data'] = plain
    printjson(result, output)
    return True

def analise_model(terms, output):
    if globals()['is_query']:
        return query(terms, output)
    
    return True

def query(terms, output):
    return True

def report(data, output):
    return True

def printjson(data, output):
    with io.open(output, 'w', encoding='utf8') as outfile:
        data['time'] = time()
        text = json.dumps(data,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)

if __name__ == '__main__':
    status = 1
    input_file = ''
    output_file = ''
    while True:
        if status == 1:
            input_file  = os.path.pardir + '/json/out.ui.json'
            output_file = os.path.pardir + '/json/in.text.json'
        elif status == 2:
            input_file = os.path.pardir + '/json/out.text.json'
            output_file = os.path.pardir + '/json/in.index.json'
        else:
            input_file = os.path.pardir + '/json/out.index.json'
            output_file = os.path.pardir + '/json/in.ui.json'

        try:
            with io.open(input_file, 'r', encoding='utf8') as data_file:
                data = json.load(data_file)
                if time() <= data['time'] + 20:
                    if process(data, status, output_file):
                        status = status + 1
                    if status > 3:
                        status = 1
        except:
            pass