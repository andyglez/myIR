import json
import io
import os
from time import time
import combine
import math

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
    result = {}
    result['action'] = 'create'
    result['data'] = []
    total = 5 if terms.__len__() >= 5 else terms.__len__() - 1
    n = terms.__len__()
    perm = math.factorial(n)
    for i in range(1, total):
        k = total - i
        variations = perm / math.factorial(n - k)
        for cb in combine.combinations(terms, total - i):
            index = {}
            word = combine.str_concat(cb)
            index['key'] = word
            index['layer'] = i
            index['idf'] = get_idf(word)
            index['documents'] = get_tf(word, variations)
            if i < total - 1:
                index['next'] = []
                count = math.factorial(total - i)
                for prox in combine.combinations(cb, total - (i + 1)):
                    edge = {}
                    edge['activation'] = math.sqrt(count) / count
                    edge['name'] = combine.str_concat(prox)
                    index['next'].append(edge)
            result['data'].append(index)
    printjson(result, output)
    return True

def get_tf(word, total):
    result = []
    for f in os.scandir(globals()['path']):
        with io.open(f, 'r', encoding='utf8') as file:
            text = ''
            for line in file.readlines():
                text = text + line + ' '
            data = {}
            data['name'] = f
            data['tf'] = text.count(word) / total
            result.append(data)
    return result

def get_idf(word):
    count_docs = 0
    count_exis = 0
    for f in os.scandir(globals()['path']):
        with io.open(f, 'r', encoding='utf8') as file:
            count_docs = count_docs + 1
            text = ''
            for line in file.readlines():
                text = text + line + ' '
            if text.count(word) > 0:
                count_exis = count_exis + 1
    return math.log10(count_docs / count_exis)

def query(terms, output):
    result = {}
    result['action'] = 'get'
    result['key'] = combine.str_concat(terms)
    printjson(result, output)
    return True

def report(data, output):
    if data['success']:
        data['action'] = 'report'
        printjson(data, output)
        return True
    return False

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