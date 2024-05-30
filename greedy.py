def nearest_neighbor_algorithm(distance_matrix, cities, start=0):
    n = len(distance_matrix)
    visited = [False] * n
    path = [start]
    visited[start] = True
    total_distance = 0

    current_city = start
    for _ in range(n - 1):
        nearest_city = None
        nearest_distance = float('inf')

        for city in range(n):
            if not visited[city] and 0 < distance_matrix[current_city][city] < nearest_distance:
                nearest_distance = distance_matrix[current_city][city]
                nearest_city = city

        path.append(nearest_city)
        visited[nearest_city] = True
        total_distance += nearest_distance
        current_city = nearest_city

    total_distance += distance_matrix[current_city][start]
    path.append(start)

    city_path = [cities[i] for i in path]
    return city_path, total_distance
