import json
import numpy as np

def main(filepath):
    with open(filepath, "r") as file:
        graph_data = json.load(file)
    nodes = graph_data["nodes"]
    num_nodes = len(nodes)
    adjacency_matrix = np.zeros((num_nodes, num_nodes))
    
    for idx, (node, connections) in enumerate(nodes.items(), start=1):
        for connected_node in connections:
            adjacency_matrix[idx - 1][int(connected_node) - 1] = 1

    extension_matrix = adjacency_matrix.copy()

    def propagate_paths(source, destination):
        for intermediate in range(num_nodes):
            if extension_matrix[destination, intermediate] != 0:
                if extension_matrix[source, intermediate] == 0:
                    extension_matrix[source, intermediate] = 2
                else:
                    extension_matrix[source, intermediate] += 1
                propagate_paths(source, intermediate)

    direct_connections = 0
    for source in range(num_nodes):
        for destination in range(num_nodes):
            if adjacency_matrix[source][destination] == 1:
                direct_connections += 1
            if extension_matrix[source][destination] != 0:
                propagate_paths(source, destination)

    entropy = 0
    for row in range(num_nodes):
        for col in range(direct_connections):
            if extension_matrix[row][col] != 0:
                prob = extension_matrix[row][col] / (num_nodes - 1)
                entropy += prob * np.log2(prob)
    
    return round(-entropy, 1)