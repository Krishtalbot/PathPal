from flask import Flask, render_template, request, redirect, url_for
import csv
import math
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
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
        total_cost_str = f"{math.floor(total_cost / 60)} hours {total_cost % 60} minutes"

    city_path_str = " ➔ ".join(city_path)

    initial_G = create_graph_with_all_edges(selected_cities, distance_matrix)
    optimized_G = create_graph_with_path(city_path, selected_cities, distance_matrix)
    
    initial_img = draw_graph(initial_G, start_city, background=False)
    optimized_img = draw_graph(optimized_G, start_city, background=False)
    optimized_img_with_bg = draw_graph(optimized_G, start_city, background=True)
    
    return render_template('results.html', city_path=city_path_str, total_cost=total_cost_str,
                           initial_img=initial_img, optimized_img=optimized_img, optimized_img_with_bg=optimized_img_with_bg)

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

def draw_graph(G, start_city, background=False):
    pos = nx.spring_layout(G)
    node_colors = ['#00A08F' if node == start_city else '#FF9F52' for node in G.nodes]

    fig, ax = plt.subplots()
    
    if background:
        img_path = os.path.join(os.path.dirname(__file__), 'static', 'img', 'Nepal Map.png')
        if os.path.exists(img_path):
            img = plt.imread(img_path)
            img_height, img_width = img.shape[0], img.shape[1]
            aspect_ratio = img_width / img_height

            
            extent_width = 1.5 * aspect_ratio  
            extent_height = 1.5  
            ax.imshow(img, aspect='auto', extent=[-extent_width/2.5, extent_width/2.5, -extent_height/2.5, extent_height/2.5], interpolation='lanczos')

           
            ax.set_xlim(-extent_width/2, extent_width/2)
            ax.set_ylim(-extent_height/2, extent_height/2)

    ax.grid(False)  # Disable grid lines
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=3000, font_size=10, font_weight="bold", ax=ax)
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    # No title set here

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"data:image/png;base64,{data}"




if __name__ == '__main__':
    app.run(debug=True)
