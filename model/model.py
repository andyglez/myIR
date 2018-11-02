import json
import io
import os
from time import time
from converter import convert
from weight import tf, idf, matrix, n_matrix
import math
import sys


def process(data, config, output):
    if config['status'] == 1:
        get_terms(data, config, output)
    elif config['status'] == 2:
        analize_model(data['terms'], config, output)
    else:
        report(data, config, output)

def get_terms(data, config, output):
    if data['action'] == 'build':
        config['is_query'] = False
        config['path'] = data['path']
        config['docs'] = [x.name for x in os.scandir(data['path']) if os.path.isfile(x)]
        scan(data['path'], output)
        printjson(config, config['current'])
    else:
        config['query_count'] = int(data['count'])
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


def analize_model(term_list, config, output):
    if config['is_query']:
        return query(term_list, config, output)

    config['terms'] = term_list
    printjson(config, config['current'])

    t_len = len(term_list)
    d_len = len([x for x in os.scandir(config['path'])])
    result = {'action': 'create',
              'path': config['path'],
              'data': [matrix(t_len * 2, t_len), n_matrix(t_len * 2), matrix(d_len, t_len * 2)],
              'tf': [tf(config['path'], x, t_len) for x in term_list],
              'idf': [idf(config['path'], x) for x in term_list]}
    printjson(result, output)


def query(term_list, config, output):
    result = {'action': 'get',
              'key': create_vector(config['terms'], term_list)}
    printjson(result, output)


def create_vector(all_terms, query_terms):
    res = []
    for term in all_terms:
        if term in query_terms:
            res.append(1)
        else:
            res.append(0)
    return res


def report(data, config, output):
    docs = [{'name': config['docs'][i], 'activation': data['results'][i]} for i in range(len(data['results'])) if data['results'][i] > 0.2] if 'results' in data else []
    res = sort(docs, config['query_count'])
    result = {'success': True, 'action': 'report', 'type': 'query' if config['is_query'] else 'build', 'results': res}
    printjson(result, output)


def sort(rank, count):
    aux = rank.copy()
    for i in range(len(aux)):
        for j in range(i + 1, len(aux)):
            if aux[i]['activation'] < aux[j]['activation']:
                swap = aux[i]
                aux[i] = aux[j]
                aux[j] = swap
    return [x for j, x in enumerate(aux) if j < count]


def printjson(dic, output):
    with io.open(output, 'w', encoding='utf8') as outfile:
        dic['time'] = time()
        text = json.dumps(dic,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)


def decide_io(status):
    if status == 1:
        return 'out.ui.json', 'in.text.json'
    if status == 2:
        return 'out.text.json', 'in.index.json'
    return 'out.index.json', 'in.ui.json'

if __name__ == '__main__':
    status = int(sys.argv[1])
    (i, o) = decide_io(status)
    input_file = os.path.curdir + '/json/' + i
    output_file = os.path.curdir + '/json/' + o
    t = time()
    config = {}
    try:
        with io.open(os.path.curdir + '/model/config.json', 'r', encoding='utf8') as config_file:
            config = json.load(config_file)
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