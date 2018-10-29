import io
import json
import os
from time import time


def process(data):
    result = {'success' : True}
    if data['action'] == 'create':
        globals()['index'] = create_index(data['data'])
    elif data['action'] == 'add' or data['action'] == 'update':
        globals()['index'][data['key']] = data['value']
    elif data['action'] == 'delete':
        globals()['index'].pop(data['key'])
    else:
        result['results'] = get(data['key'])
    printjson(result, os.path.pardir + '/json/out.index.json')

def get(key):
    value = [(0, globals()['index'][key])]
    aux = []
    while value.__len__() > 0:
        (activation, node) = value.pop()
        if 'next' in node:
            for nxt in node['next']:
                value.append((activation + nxt['activation'], globals()['index'][nxt['name']]))
        else:
            idf = node['idf']
            for document in node['documents']:
                activation = activation + (document['tf'] * idf)
            aux.append({'activation': activation, 'documents': [doc for doc in node['documents']]})
    aux = sort(aux)
    return aux

def sort(value):
    aux = []
    for node in value:
        for doc in node['documents']:
            temp = [t for t in aux if t['name'] == doc['name']]
            if temp.__len__() == 0:
                h = {}
                h['activation'] = node['activation'] * doc['tf']
                h['name'] = doc['name']
                aux.append(h)
            else:
                for a in aux:
                    if a['name'] == doc['name']:
                        a['activation'] = a['activation'] + node['activation'] * doc['tf']

    #aux = value.copy()
    #for i in range(aux.__len__()):
    #    for j in range(i + 1, aux.__len__()):
    #        a = aux[i]['activation']
    #        b = aux[j]['activation']
    #        if b < a:
    #            temp = aux[i]
    #            aux[i] = aux[j]
    #            aux[j] = temp
    return aux

def create_index(data):
    result = {}
    for node in data:
        result[node['key']] = node
    return result

def printjson(data, output):
    data['time'] = time()
    text = json.dumps(data,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    with io.open(output, 'w', encoding='utf8') as outfile:
        outfile.write(text)

if __name__ == '__main__':
    globals()['index'] = {}
    t = time()
    while True:
        try:
            data = {}
            with io.open(os.path.pardir + '/json/in.index.json', 'r', encoding='utf8') as data_file:
                data = json.load(data_file)
            if t < data['time']:
                process(data)
                t = time()
        except Exception as e:
            printjson({'success': False, 'message': str(e)}, os.path.pardir + '/json/out.index.json')
            pass