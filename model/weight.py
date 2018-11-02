from converter import convert
from os import scandir, urandom
from math import log2, pow, sqrt

def tf(path, word, total):
    result = []
    for f in scandir(path):
        text = convert(f)
        tf = text.count(word) / total
        if tf > 0:
            data = {}
            data['name'] = f.name
            data['tf'] = text.count(word) / total
            result.append(data)
    return result


def idf(path, word):
    count_docs = 0
    count_exis = 0
    for f in scandir(path):
        text = convert(f)
        count_docs = count_docs + 1
        if text.count(word) > 0:
            count_exis = count_exis + 1
    return 0 if count_exis == 0 else log2(count_docs / count_exis)


def matrix(n):
    return matrix(n, n)


def matrix(n, m):
    return [normalize([urandom(m) for _ in range(m)]) for _ in range(n)]


def normalize(weights):
    den = normal_denominator(weights)
    return [w / den for w in weights]


def normal_denominator(weights):
    den = 0
    for x in [pow(w, 2) for w in weights]:
        den += x
    return sqrt(den)