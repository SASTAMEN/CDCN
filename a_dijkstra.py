V = 9
INF = float('inf')  # Use infinity to represent no connection

# Function to find the vertex with the smallest distance
def minDistance(dist, sptSet):
    min_val = INF
    min_index = -1
    for v in range(V):
        if not sptSet[v] and dist[v] <= min_val:
            min_val = dist[v]
            min_index = v
    return min_index

# Dijkstra's Algorithm
def dijkstra(graph, src):
    dist = [INF] * V  # Initialize distances as infinite
    sptSet = [False] * V  # Track vertices included in shortest path tree
    parent = [-1] * V  # Store the path for each vertex

    dist[src] = 0  # Distance to source is 0

    for _ in range(V - 1):
        u = minDistance(dist, sptSet)  # Pick the minimum distance vertex
        sptSet[u] = True

        for v in range(V):
            if (
                not sptSet[v]
                and graph[u][v]
                and dist[u] != INF
                and dist[u] + graph[u][v] < dist[v]
            ):
                dist[v] = dist[u] + graph[u][v]
                parent[v] = u  # Update parent for path tracking

    return dist, parent

# Function to extract the paths from the parent array
def extract_paths(parent, src):
    paths = []
    for i in range(V):
        path = []
        current = i
        while current != -1:
            path.insert(0, current)
            current = parent[current]
        if path[0] == src:  # Valid path from the source
            paths.append((i, path))
    return paths

# Function to print paths
def print_paths(paths, distances, graph_title):
    print(f"\nShortest Paths for {graph_title}:")
    for vertex, path in paths:
        print(f"Path to {vertex}: {' -> '.join(map(str, path))} (Distance: {distances[vertex]})")

# Example Graph 1
graph1 = [
    [0, 4, 0, 0, 0, 0, 0, 8, 0],
    [4, 0, 8, 0, 0, 0, 0, 11, 0],
    [0, 8, 0, 7, 0, 4, 0, 0, 2],
    [0, 0, 7, 0, 9, 14, 0, 0, 0],
    [0, 0, 0, 9, 0, 10, 0, 0, 0],
    [0, 0, 4, 14, 10, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 1, 6],
    [8, 11, 0, 0, 0, 0, 1, 0, 7],
    [0, 0, 2, 0, 0, 0, 6, 7, 0],
]

# Example Graph 2
graph2 = [
    [0, 2, 0, 1, 0, 0, 0, 0, 0],
    [2, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 7, 0, 0, 4, 0],
    [1, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 7, 2, 0, 5, 0, 0, 1],
    [0, 0, 0, 0, 5, 0, 6, 0, 0],
    [0, 0, 0, 0, 0, 6, 0, 0, 8],
    [0, 0, 4, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 1, 0, 8, 3, 0],
]

# Run Dijkstra's for Graph 1
distances1, parent1 = dijkstra(graph1, 0)
paths1 = extract_paths(parent1, 0)
print_paths(paths1, distances1, "Graph 1")

# Run Dijkstra's for Graph 2
distances2, parent2 = dijkstra(graph2, 0)
paths2 = extract_paths(parent2, 0)
print_paths(paths2, distances2, "Graph 2")
