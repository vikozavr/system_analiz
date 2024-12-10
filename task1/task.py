import json
import numpy as np

def main(file_path):

    with open(file_path, "r") as file:
        content = json.load(file)

    vertices = content.get("nodes", {})
    size = len(vertices)
    adjacency_matrix = np.zeros((size, size))

    
    for node, neighbors in vertices.items():
        node_index = int(node) - 1
        for neighbor in neighbors:
            neighbor_index = int(neighbor) - 1
            adjacency_matrix[node_index][neighbor_index] = 1

    
    return adjacency_matrix

#if __name__ == "__main__":
    #adjacency_matrix = main('file_path.json')
    #print("Adjacency Matrix:")
    #print(adjacency_matrix)