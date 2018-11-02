import io
import json
import os
import neural_network as nn
from time import time


def process(data, index):
    result = {'success' : True}
    if data['action'] == 'create':
        create_index(data, index)
    elif data['action'] == 'add' or data['action'] == 'update':
        globals()['index'][data['key']] = data['value']
    elif data['action'] == 'delete':
        globals()['index'].pop(data['key'])
    else:
        result['results'] = get(index['data'], data['key'])
    printjson(result, os.path.curdir + '/json/out.index.json')


def get(network, input_vector):
    return nn.feed_forward(network, input_vector)[-1]


def create_index(data, index):
    neural_network = data['data']
    index['data'] = nn.train(neural_network, data['tf'], data['idf'])
    printjson(index, index['current'])


def printjson(data, output):
    data['time'] = time()
    text = json.dumps(data,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    with io.open(output, 'w', encoding='utf8') as outfile:
        outfile.write(text)

if __name__ == '__main__':
    index = {}
    try:
        with io.open(os.path.curdir + '/index/index.json', 'r', encoding='utf8') as model:
            index = json.load(model)
            index['current'] = os.path.curdir + '/index/index.json'
    except:
        pass
    try:
        data = {}
        with io.open(os.path.curdir + '/json/in.index.json', 'r', encoding='utf8') as data_file:
            data = json.load(data_file)
        process(data, index)
    except Exception as e:
        print(e)
        pass