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
    return res


def build_targets(tfs, idfs):
    res = []
    for idf, tf_i in zip(idfs, tfs):
        aux = []
        for tf in tf_i:
            if idf * tf > 0:
                aux.append(1)
            else:
                aux.append(0)
        res.append(aux)
    return res


def normal_denominator(weights):
    den = 1
    for x in [pow(w, 2) for w in weights]:
        den += x
    return sqrt(den)
