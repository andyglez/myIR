from math import sqrt


def build_inputs(length):
    res = []
    for i in range(length):
        aux = []
        for j in range(length):
            if i == j:
                aux.append(1)
            else:
                aux.append(0)
        res.append(aux)

    a = []
    b = []
    for i in range(length):
        a.append(1)
        b.append(0)
    res.append(a)
    res.append(b)

    return res


def build_targets(tfs, idfs):
    res = []
    for idf, tf_i in zip(idfs, tfs):
        aux = []
        for tf in tf_i:
            aux.append(tf * idf)
        res.append(normalize(aux))

    a = []
    b = []
    for tf_i in tfs:
        for tf in tf_i:
            a.append(1)
            b.append(0)
        break
    res.append(a)
    res.append(b)
    return res

def normalize(weights):
    den = normal_denominator(weights)
    return [w / den for w in weights]

def normal_denominator(weights):
    den = 1
    for x in [pow(w, 2) for w in weights]:
        den += x
    return sqrt(den)
