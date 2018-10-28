def list_concat(x, y):
    ret = x.copy()
    for comb in y:
        ret.append(comb)
    return ret

def str_concat(x):
    result = ''
    for word in x:
        result = result + word + ' '
    return result[:-1]

def permutations(l):
    for item in l:
        if len(l) == 1:
            yield [item]
        for perm in permutations([other for other in l if other != item]):
            yield list_concat([item], perm)


def combinations(l, k):
    for item in l:
        if k == 1:
            yield [item]
        for comb in combinations([other for other in l if other != item], k - 1):
            yield list_concat([item], comb)