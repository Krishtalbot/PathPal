import matplotlib.pyplot as plt
import networkx as nx
from greedy import nearest_neighbor_algorithm
import csv
import math

def read_csv(file_path):
    with open(file_path, mode='r') as infile:
        reader = csv.reader(infile)
        data = list(reader)
        
    headers = data[0]
    distance_matrix = {row[0]: {headers[i]: int(row[i]) for i in range(1, len(headers))} for row in data[1:]}
    return headers[1:], distance_matrix


def get_user_destinations(all_destinations):
    destination_dict = {i+1: dest for i, dest in enumerate(all_destinations)}
    print("\nAvailable destinations: ")
    for num, dest in destination_dict.items():
        print(f"{num}: {dest}")
    
    selected_numbers = input("\nEnter the numbers corresponding to the destinations you want to visit, separated by space (First place selected is the starting place): ").split()
    selected_numbers = [int(num.strip()) for num in selected_numbers]
    
    selected_destinations = [destination_dict[num] for num in selected_numbers if num in destination_dict]
    return selected_destinations


def generate_distance_matrix(selected_destinations, distance_data):
    n = len(selected_destinations)
    distance_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            distance_matrix[i][j] = distance_data[selected_destinations[i]][selected_destinations[j]]
    return distance_matrix

def measure_input():
    measure = int(input("\nOptimize based on:\n1.Distance\n2.Time\n"))
    if measure == 1:
        all_destinations, distance_data = read_csv('distance_cost.csv')
    elif measure == 2:
        all_destinations, distance_data = read_csv('time_cost.csv')
    else:
        print("Please select appropriate input.")
        measure_input()
    return all_destinations, distance_data, measure

cities_data, distance_data, measure = measure_input()
cities = get_user_destinations(cities_data)
distance_matrix = generate_distance_matrix(cities, distance_data)
    
print("\n\nCities: ", cities)
print("\nDistance Matrix: ")
for row in distance_matrix:
    print(row)

'''cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
distance_matrix = [
    [0, 2795, 790, 1627, 2445],
    [2795, 0, 2015, 1547, 372],
    [790, 2015, 0, 1084, 1745],
    [1627, 1547, 1084, 0, 1174],
    [2445, 372, 1745, 1174, 0]
]'''

start_city_index = 0
city_path, total_cost = nearest_neighbor_algorithm(distance_matrix, cities, start_city_index)

print("\n\nTravel Path:", city_path)
if measure == 1:
    print("Total Distance:", total_cost, "kilometers")
elif measure == 2:
    print("Total Time:", math.floor(total_cost/60), "hours", (total_cost%60))

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