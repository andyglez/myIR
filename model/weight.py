from math import log2, pow, sqrt
from random import randint


def tf(docs, word, total):
    result = []
    for doc in docs:
        value = doc.count(word.upper()) / total
        result.append(value)
    return result


def idf(docs, word):
    count_docs = 0
    count_exis = 0
    for doc in docs:
        count_docs = count_docs + 1
        if doc.count(word.upper()) > 0:
            count_exis = count_exis + 1
    return 0 if count_exis == 0 else log2(count_docs / count_exis)


def n_matrix(n):
    return matrix(n, n)


def matrix(n, m):
    return [normalize([randint(0, n*m) for j in range(m)]) for i in range(n)]


def normalize(weights):
    den = normal_denominator(weights)
    return [w / den for w in weights]


def normal_denominator(weights):
    den = 0
    for x in [pow(w, 2) for w in weights]:
        den += x
    return sqrt(den)