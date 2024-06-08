import itertools

def held_karp(dists):
    n = len(dists)
    C = {}

    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)

    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = sum(1 << bit for bit in subset)
            for k in subset:
                prev_bits = bits & ~(1 << k)
                res = [(C[(prev_bits, m)][0] + dists[m][k], m) for m in subset if m != k]
                C[(bits, k)] = min(res)

    bits = (1 << n) - 2
    res = [(C[(bits, k)][0] + dists[k][0], k) for k in range(1, n)]
    opt, parent = min(res)

    # Reconstruct the path
    path = [0]
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    path.append(0)

    return opt, path

def generate_distances(locations, distances):
    n = len(locations)
    dists = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            dists[i][j] = dists[j][i] = distances[locations[i]][locations[j]]

    return dists
