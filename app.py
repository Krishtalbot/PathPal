from flask import Flask, render_template, request, redirect, url_for
import csv
import math
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from greedy import nearest_neighbor_algorithm

app = Flask(__name__)

def read_csv(file_path):
    with open(file_path, mode='r') as infile:
        reader = csv.reader(infile)
        data = list(reader)
    headers = data[0]
    distance_matrix = {row[0]: {headers[i]: int(row[i]) for i in range(1, len(headers))} for row in data[1:]}
    return headers[1:], distance_matrix

def generate_distance_matrix(selected_destinations, distance_data):
    n = len(selected_destinations)
    distance_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            distance_matrix[i][j] = distance_data[selected_destinations[i]][selected_destinations[j]]
    return distance_matrix

@app.route('/', methods=['GET', 'POST'])
def index():
    all_destinations, _ = read_csv('distance_cost.csv')  # Just to get the list of cities
    return render_template('index.html', cities=all_destinations)

@app.route('/select_cities', methods=['POST'])
def select_cities():
    selected_cities = request.form.getlist('cities')
    if len(selected_cities) < 2:
        return "Please select at least two cities to calculate a route."

    start_city = request.form['start_city']
    if start_city not in selected_cities:
        return "The start city must be one of the selected cities."

    measure = request.form['measure']
    
    if measure == 'distance':
        _, distance_data = read_csv('distance_cost.csv')
    elif measure == 'time':
        _, distance_data = read_csv('time_cost.csv')
    
    distance_matrix = generate_distance_matrix(selected_cities, distance_data)
    
    start_city_index = selected_cities.index(start_city)
    city_path, total_cost = nearest_neighbor_algorithm(distance_matrix, selected_cities, start_city_index)

    if measure == 'distance':
        total_cost_str = f"{total_cost} kilometers"
    elif measure == 'time':
        total_cost_str = f"{math.floor(total_cost/60)} hours {(total_cost % 60)} minutes"

    initial_G = create_graph_with_all_edges(selected_cities, distance_matrix)
    optimized_G = create_graph_with_path(city_path, selected_cities, distance_matrix)
    
    initial_img = draw_graph(initial_G, "Initial Graph", start_city)
    optimized_img = draw_graph(optimized_G, "Optimized Path Graph", start_city)
    
    return render_template('results.html', city_path=city_path, total_cost=total_cost_str,
                           initial_img=initial_img, optimized_img=optimized_img)

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

def draw_graph(G, title, start_city):
    pos = nx.spring_layout(G)
    node_colors = ['#00A08F' if node == start_city else '#FF9F52' for node in G.nodes]
    plt.figure()
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=3000, font_size=10, font_weight="bold")
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(title)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"data:image/png;base64,{data}"

if __name__ == '__main__':
    app.run(debug=True)
