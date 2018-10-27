import json
import io
import os
from time import time

def process(data, state, output):
    return True

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