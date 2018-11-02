import json
import io
import os
from time import time
from converter import convert
from weigth import tf, idf, matrix
import math
import sys


def process(data, config, output):
    if config['status'] == 1:
        get_terms(data, output)
    elif config['status'] == 2:
        analize_model(data['terms'], output)
    else:
        report(data, output)

def get_terms(data, output):
    if data['action'] == 'build':
        config['is_query'] = False
        config['path'] = data['path']
        config['docs'] = [x for x in os.scandir(data['path']) if os.path.isfile(x)]
        scan(data['path'], output)
        printjson(config, config['current'])
    else:
        config['query_count'] = data['count']
        config['is_query'] = True
        terms(data['query'], output)
        printjson(config, config['current'])


def scan(path, output):
    try:
        plain = ''
        for f in [x for x in os.scandir(path) if os.path.isfile(x)]:
            plain = plain + convert(f)
        terms(plain, output)
    except:
        pass


def terms(plain, output):
    printjson({'action': 'process', 'data': plain}, output)


def analize_model(term_list, output):
    if config['is_query']:
        return query(term_list, output)

    config['terms'] = term_list
    printjson(config, config['current'])

    t_len = len(term_list)
    d_len = len(os.scandir(config['path']))
    result = {'action': 'create',
              'path': config['path'],
              'data': [matrix(t_len * 2, t_len), matrix(t_len * 2), matrix(t_len * 2, d_len)],
              'tf': [tf(x) for x in term_list],
              'idf': [idf(x) for x in term_list]}
    printjson(result, output)


def query(term_list, output):
    result = {}
    result['action'] = 'get'
    result['key'] = [1 for term in config['terms'] if term in term_list and 0 if term not in term_list]
    printjson(result, output)


def report(data, output):
    docs = [config['docs'][i] for i in range(len(data['results'])) if data['results'][i] > 0.2]
    result = {'success': True, 'action': 'report', 'type': 'query' if config['is_query'] else 'build', 'results': docs}
    printjson(result, output)

def printjson(data, output):
    with io.open(output, 'w', encoding='utf8') as outfile:
        data['time'] = time()
        text = json.dumps(data,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)

if __name__ == '__main__':
    status = int(sys.argv[1])
    input_file = os.path.curdir + '/json/'
    output_file = os.path.curdir + '/json/'
    if status == 1:
        input_file = input_file + 'out.ui.json'
        output_file= output_file+ 'in.text.json'
    elif status == 2:
        input_file = input_file + 'out.text.json'
        output_file= output_file+ 'in.index.json'
    else:
        input_file = input_file + 'out.index.json'
        output_file= output_file+ 'in.ui.json'
    t = time()
    config = {}
    try:
        with io.open(os.path.curdir + '/model/config.json', 'r', encoding='utf8') as config:
            c = json.load(config)
            if 'time' in c:
                config = c
    except:
        pass
    config['status'] = status
    config['current'] = os.path.curdir + '/model/config.json'
    try:
        data = {}
        with io.open(input_file, 'r', encoding='utf8') as file:
            data = json.load(file)
        process(data, config, output_file)
    except:
        pass