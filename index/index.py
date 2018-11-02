import io
import json
import os
from time import time
from numpy import dot


def process(data, index):
    result = {'success' : True}
    if data['action'] == 'create':
        create_index(data, index)
    elif data['action'] == 'add' or data['action'] == 'update':
        globals()['index'][data['key']] = data['value']
    elif data['action'] == 'delete':
        globals()['index'].pop(data['key'])
    else:
        result['results'] = get(data['key'])
    printjson(result, os.path.curdir + '/json/out.index.json')

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


def create_index(data, index):
    neural_network = data['data']
    index['data'] = train(neural_network, data['tf'], data['idf'])
    printjson(index, index['path'])


def train(neural_network, tf, idf):
    inputs = [[1 for j in range(len(tf)) if j == i and 0 if not j == i] for i in range(len(tf))]
    targets = [[1 for tf in tf_i if idf * tf > 0 and 0 if idf * tf == 0] for idf, tf_i in zip(idf, tf)]

    for i in range(10):
        for input_vector, target_vector in zip(inputs, targets):
            backpropagate(neural_network, input_vector, target_vector)
    return neural_network


def backpropagate(neural_network, input_vector, targets):
    outputs = feed_forward(neural_network, input_vector)
    outputs.insert(0, input_vector)
    count = 1
    while len(outputs) > 1:
        output_deltas = [output * (1 - output) * (output - target)
                         for output, target in zip(outputs[-1], targets)]

        for i, output_neuron in enumerate(neural_network[-count]):
            for j, prev_output in enumerate(outputs[-1]):
                output_neuron[j] -= output_deltas[i] * prev_output

        prev_deltas = [prev_output * (1 - prev_output) *
                       dot(output_deltas, [n[i] for n in neural_network[-count]])
                       for i, prev_output in enumerate(neural_network[-(count+1)])]

        outputs.remove(outputs[-1])
        count += 1
        targets = []

        for i, prev_neuron in enumerate(outputs[-1]):
            targets.append(prev_neuron - prev_deltas * outputs[-2])


def feed_forward(neural_network, input_vector):
    return 0


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
    except:
        pass