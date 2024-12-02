import json
import numpy as np

def process_json_file(file_path):
    with open(file_path, "r") as file:
        graph_data = json.load(file)
    
    node_data = graph_data["nodes"]
    node_count = len(node_data)
    
    
    adjacency_matrix = np.zeros((node_count, node_count))

    for node, connections in node_data.items():
        node_idx = int(node) - 1
        for connected_node in connections:
            connected_idx = int(connected_node) - 1
            adjacency_matrix[node_idx][connected_idx] = 1
            adjacency_matrix[connected_idx][node_idx] = -1

    
    results = np.zeros((5, node_count))

    
    def search_connections(out_function, connection_type):
        visited = set()

        def search(row, col):
            nonlocal visited
            for neighbor in range(node_count):
                if adjacency_matrix[col][neighbor] == connection_type and neighbor not in visited:
                    visited.add(neighbor)
                    out_function(row)
                    search(row, neighbor)

        return search

    search_out = search_connections(lambda idx: results[2, idx] + 1, 1)
    search_in = search_connections(lambda idx: results[3, idx] + 1, -1)

    for i in range(node_count):
        for j in range(node_count):
            if adjacency_matrix[i][j] == 1:
                results[0][i] += 1
            elif adjacency_matrix[i][j] == -1:
                results[1][i] += 1
        
        search_out(i, i)
        search_in(i, i)

        for j in range(node_count):
            if adjacency_matrix[i][j] == 1 and i != j:
                results[4][i] += 1

    return results