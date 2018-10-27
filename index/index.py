import io
import json
import os
from time import time


def process(data, index):
    if data['action'] == 'create':
        index = data['data']
    elif data['action'] == 'add' or data['action'] == 'update':
        index[data['key']] = data['value']
    elif data['action'] == 'delete':
        index.pop(data['key'])
    else:
        get(data['key'], index)

def get(key, index):
    result = {}
    result['success'] = True
    result['value'] = index[key]
    result['time'] = time()
    with io.open(os.path.pardir + '/json/out.index.json', 'w', encoding='utf8') as outfile:
        text = json.dumps(result,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)
    return result

if __name__ == '__main__':
    index = {}
    while True:
        try:
            with io.open(os.path.pardir + '/json/in.index.json', 'r', encoding='utf8') as data_file:
                data = json.load(data_file)
                if time() <= data['time'] + 20:
                    process(data, index)
        except:
            pass