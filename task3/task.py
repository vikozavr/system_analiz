import json
import numpy as np

def main(file_path):
    
    with open(file_path, "r") as file:
        data = json.load(file)
    
    nodes = data.get("nodes", {})
    node_count = len(nodes)
    
    
    adjacency_matrix = np.zeros((node_count, node_count))
    for node, connections in nodes.items():
        node_idx = int(node) - 1
        for connected_node in connections:
            connected_idx = int(connected_node) - 1
            adjacency_matrix[node_idx][connected_idx] = 1
            
    
    result_matrix = np.copy(adjacency_matrix)

    
    def update_paths(start, current):
        for neighbor in range(node_count):
            if result_matrix[current, neighbor] != 0:
                result_matrix[start, neighbor] += 2 if result_matrix[start, neighbor] == 0 else 1
                update_paths(start, neighbor)

   
    for i in range(node_count):
        for j in range(node_count):
            if result_matrix[i][j] != 0:
                update_paths(i, j)

    
    total_connections = (adjacency_matrix > 0).sum()

    
    entropy_sum = 0
    for j in range(node_count):
        for i in range(node_count): 
            if result_matrix[j][i] != 0:
                prob = result_matrix[j][i] / (node_count - 1)
                entropy_sum += prob * np.log2(prob)
    
    
    entropy_sum = round(-entropy_sum, 1)

    return entropy_sum