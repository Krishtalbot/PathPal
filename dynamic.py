import itertools
import sys
import networkx as nx
import matplotlib.pyplot as plt
import random

def held_karp(dists):
    n = len(dists)

    C = {}

    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)

    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)

    bits = (2**n - 1) - 1

    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    path.append(0)

    return opt, list(reversed(path))


def generate_distances(locations, distances):
    n = len(locations)
    dists = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            dists[i][j] = dists[j][i] = distances[locations[i]][locations[j]]

    return dists


if __name__ == '__main__':
    locations = [
        "Kathmandu", "Pokhara", "Chitwan", "Lumbini", "Annapurna Base Camp"
    ]

    distances = {
        "Kathmandu": {"Pokhara": 200, "Chitwan": 150, "Lumbini": 300, "Annapurna Base Camp": 500},
        "Pokhara": {"Chitwan": 250, "Lumbini": 350, "Annapurna Base Camp": 400},
        "Chitwan": {"Lumbini": 180, "Annapurna Base Camp": 700},
        "Lumbini": {"Annapurna Base Camp": 600},
    }

    dists = generate_distances(locations, distances)

    for row in dists:
        print(''.join([str(n).rjust(5, ' ') for n in row]))

    print('')

    opt, path = held_karp(dists)
    print("Optimal Cost:", opt)
    print("Optimal Path:", path)

    random.seed(42)

    G = nx.Graph()
    for i, loc in enumerate(locations):
        G.add_node(i, label=loc)

    for i in range(len(dists)):
        for j in range(i + 1, len(dists[i])):
            G.add_edge(i, j, weight=dists[i][j])

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    pos = nx.spring_layout(G, seed=42)  # Fixed layout seed
    nx.draw(G, pos, with_labels=True, node_color=['salmon' if node == 0 else 'skyblue' for node in G.nodes()],
            node_size=1500, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): G[u][v]['weight'] for u, v in G.edges()}, font_size=8)
    plt.title("Original Graph with Weighted Edges")

    G_solution = nx.DiGraph()
    for i, loc in enumerate(locations):
        G_solution.add_node(i, label=loc)

    for i in range(len(path) - 1):
        G_solution.add_edge(path[i], path[i + 1])

    G_solution.add_edge(path[-1], path[0])

    plt.subplot(1, 2, 2)
    nx.draw(G_solution, pos, with_labels=True, arrows=True,
            node_color=['salmon' if node == path[0] else 'lightgreen' for node in G_solution.nodes()],
            node_size=1500, font_size=10, font_weight='bold')
    plt.title("Solution Graph")

    plt.tight_layout()
    plt.show()
