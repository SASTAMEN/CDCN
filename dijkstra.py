import heapq

# Input the graph
n = int(input("Enter the total number of nodes in the graph: "))
print("Enter the adjacency matrix of the graph (Enter -1 if no link exists):")
adjacency_matrix = []
for i in range(n):
    row = list(map(int, input().split()))
    for j in range(n):
        if row[j] == -1:
            row[j] = float('inf')  # Replace -1 with infinity for unconnected nodes
    adjacency_matrix.append(row)

# Initialize distances and parent array
dist = [float('inf')] * n
parent = [-1] * n
dist[0] = 0

# Priority queue for Dijkstra's algorithm
pq = []
heapq.heappush(pq, (0, 0))  # (distance, node)

# Dijkstra's algorithm
while pq:
    current_dist, current_node = heapq.heappop(pq)
    for neighbor in range(n):
        if adjacency_matrix[current_node][neighbor] != float('inf'):
            distance = adjacency_matrix[current_node][neighbor]
            if dist[current_node] + distance < dist[neighbor]:
                dist[neighbor] = dist[current_node] + distance
                parent[neighbor] = current_node  # Update parent
                heapq.heappush(pq, (dist[neighbor], neighbor))

# Function to reconstruct path
def get_path(node):
    path = []
    while node != -1:
        path.append(node)
        node = parent[node]
    return path[::-1]

# Print shortest distances and paths
print("Shortest distances and paths from node 0 (source):")
for i in range(n):
    if dist[i] == float('inf'):
        print(f"Node {i}: Distance = Infinity, Path = No Path")
    else:
        path = get_path(i)
        print(f"Node {i}: Distance = {dist[i]}, Path = {' -> '.join(map(str, path))}")
