import json
import numpy as np
import operator

def main(file_path):
    with open(file_path, "r") as file:
        graph_data = json.load(file)
    
    node_data = graph_data.get("nodes", {})
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
        def search(row, col, visited):
            for neighbor in range(node_count):
                if adjacency_matrix[col][neighbor] == connection_type and neighbor not in visited:
                    visited.add(neighbor)
                    out_function(neighbor)
                    search(row, neighbor, visited)

        return search

    
    search_out = search_connections(lambda idx: operator.setitem(results[2], idx, results[2, idx] + 1), 1)
    search_in = search_connections(lambda idx: operator.setitem(results[3], idx, results[3, idx] + 1), -1)

    
    for i in range(node_count):
        for j in range(node_count):
            if adjacency_matrix[i][j] == 1:
                results[0][i] += 1
            elif adjacency_matrix[i][j] == -1:
                results[1][i] += 1
        
        visited_out = set()
        visited_in = set()
        search_out(i, i, visited_out)
        search_in(i, i, visited_in)

        for j in range(node_count):
            if adjacency_matrix[i][j] == 1 and i != j:
                results[4][i] += 1

    return results