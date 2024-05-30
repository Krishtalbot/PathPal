import matplotlib.pyplot as plt
import networkx as nx
from greedy import nearest_neighbor_algorithm

cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
distance_matrix = [
    [0, 2795, 790, 1627, 2445],
    [2795, 0, 2015, 1547, 372],
    [790, 2015, 0, 1084, 1745],
    [1627, 1547, 1084, 0, 1174],
    [2445, 372, 1745, 1174, 0]
]

start_city_index = 0
city_path, total_distance = nearest_neighbor_algorithm(distance_matrix, cities, start_city_index)

print("Travel Path:", city_path)
print("Total Distance:", total_distance, "miles")

def create_graph_with_all_edges(cities, distance_matrix):
    G = nx.Graph()
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            if distance_matrix[i][j] > 0:
                G.add_edge(cities[i], cities[j], weight=distance_matrix[i][j])
    return G

def create_graph_with_path(city_path, cities, distance_matrix):
    G = nx.DiGraph()
    for i in range(len(city_path) - 1):
        G.add_edge(city_path[i], city_path[i + 1], weight=distance_matrix[cities.index(city_path[i])][cities.index(city_path[i + 1])])
    return G

def draw_graph(G, pos, node_colors, title):
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=3000, font_color="white",
            font_size=10, font_weight="bold", font_family="Times New Roman", width=2, edge_color="#1c4755")
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(title)

initial_G = create_graph_with_all_edges(cities, distance_matrix)
initial_node_colors = ["#00A08F" if city == cities[start_city_index] else "#FF9F52" for city in cities]

optimized_G = create_graph_with_path(city_path, cities, distance_matrix)
optimized_node_colors = ["#00A08F" if city == city_path[0] else "#FF9F52" for city in cities]

plt.figure(figsize=(16, 8))  

plt.subplot(121)
pos = nx.spring_layout(initial_G)
draw_graph(initial_G, pos, initial_node_colors, "Initial Graph")

plt.subplot(122)
pos = nx.spring_layout(optimized_G)

pos = nx.spring_layout(optimized_G, pos=pos, iterations=100)  
draw_graph(optimized_G, pos, optimized_node_colors, "Optimized Path Graph")

plt.tight_layout()  
plt.show()
