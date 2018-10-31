import json
from time import time
import io
import subprocess
import os

def run_modules():
    subprocess.run(['python', os.path.curdir + '/model/model.py', '1'])
    subprocess.run(['python', os.path.curdir + '/text/process.py'])
    subprocess.run(['python', os.path.curdir + '/model/model.py', '2'])
    subprocess.run(['python', os.path.curdir + '/index/index.py'])
    subprocess.run(['python', os.path.curdir + '/model/model.py', '3'])

if __name__ == '__main__':
    t = time()
    while True:
        try:
            data = {}
            with io.open(os.path.curdir + '/json/out.ui.json', 'r', encoding='utf8') as data_file:
                data = json.load(data_file)
            if 'time' in data and t < data['time']:
                run_modules()
                t = data['time']
        except:
            pass

