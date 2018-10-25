import io
import json
import os
from time import time


def process(data):
    if data['action'] == 'create':
        create(data['data'])
    elif data['action'] == 'add':
        add(data['key'], data['value'])
    elif data['action'] == 'update':
        update(data['key'], data['value'])
    elif data['action'] == 'delete':
        delete(data['key'])
    else:
        get('key')

def create(data):
    return 0    

def add(key, value):
    return 0

def update(key, value):
    return 0

def delete(key):
    return 0

def get(key):
    return 0

if __name__ == '__main__':
    try:
        with io.open(os.path.pardir + '/json/in.index.json') as data_file:
            data = json.load(data_file)
            if time() <= data['time'] + 20:
                process(data)
    except:
        pass