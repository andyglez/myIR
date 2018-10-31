import json
import io
import os
from time import time
import combine
import math
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def process(data, state, output):
    if state == 1:
        return get_terms(data, output)
    if state == 2:
        return analise_model(data['terms'], output)
    return report(data, output)

def get_terms(data, output):
    if data['action'] == 'build':
        globals()['config']['is_query'] = False
        globals()['config']['path'] = data['path']
        printjson(globals()['config'], os.path.curdir + '/model/config.json')
        return scan(data['path'], output)
    else:
        globals()['config']['query_count'] = data['count']
        globals()['config']['is_query'] = True
        printjson(globals()['config'], os.path.curdir + '/model/config.json')
        return terms(data['query'], output)

def scan(path, output):
    try:
        plain = ''
        for file in os.scandir(path):#[x for x in os.scandir(path) if os.path.isfile(x)]:
            plain = plain + convert(file)
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
    if globals()['config']['is_query']:
        return query(terms, output)
    result = {}
    result['action'] = 'create'
    result['data'] = []
    total = 5 if terms.__len__() >= 5 else terms.__len__()
    n = terms.__len__()
    perm = math.factorial(n)
    for i in range(0, total):
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
    for f in os.scandir(globals()['config']['path']):
        text = convert(f)
        tf = text.count(word) / total
        if tf > 0:
            data = {}
            data['name'] = f.name
            data['tf'] = text.count(word) / total
            result.append(data)
    return result

def convert(f):
    text = ''
    if 'pdf' in f.name:
        text = convert_from_pdf(f)
    else:
        with io.open(f, 'r') as file:
            for line in file.readlines():
                text = text + line + ' '
    return  text

def convert_from_pdf(file_path):
    manager = PDFResourceManager()
    output = io.StringIO()
    codec = 'utf-8'
    converter = TextConverter(manager, output, codec=codec, laparams=LAParams())

    interpreter = PDFPageInterpreter(manager, converter)
    pagenums = set()
    infile = open(file_path, 'rb')

    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)

    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()

    assert isinstance(text, object)
    return str(text).replace('', '')

def get_idf(word):
    count_docs = 0
    count_exis = 0
    for f in os.scandir(globals()['config']['path']):
        text = convert(f)
        count_docs = count_docs + 1
        if text.count(word) > 0:
            count_exis = count_exis + 1
    return 0 if count_exis == 0 else math.log10(count_docs / count_exis)

def query(terms, output):
    result = {}
    result['action'] = 'get'
    result['key'] = combine.str_concat(terms)
    printjson(result, output)
    return True

def report(data, output):
    #if data['success']:
    result = {}
    result['success'] = True
    if 'results' in data:
        result['results'] = data['results']
    result['action'] = 'report'
    result['type'] = 'query' if globals()['config']['is_query'] else 'build'
    printjson(result, output)
    #else:
    #    printjson({'action': 'report', 'success': False, 'type': 'error'}, output)
    return data['success']

def printjson(data, output):
    with io.open(output, 'w', encoding='utf8') as outfile:
        data['time'] = time()
        text = json.dumps(data,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)

def has_changed(file, t):
    try:
        with io.open(os.path.pardir + file, 'r', encoding='utf8') as inp:
            data = json.load(inp)
            if 'time' in data and t <= data['time']:
                return (True, data)
    except:
        pass
    return (False, {})

def action_completed(inp, out, t, status):
    (flag, dic) = has_changed(inp, t)
    if flag:
        process(dic, status, os.path.pardir + out)
        return True
    return False

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
    try:
        with io.open(os.path.curdir + '/model/config.json', 'r', encoding='utf8') as config:
            c = json.load(config)
            if 'time' in c:
                globals()['config'] = c
            else:
                globals()['config'] = {}
    except:
        pass
    try:
        data = {}
        with io.open(input_file, 'r', encoding='utf8') as file:
            data = json.load(file)
        process(data, status, output_file)
    except:
        pass