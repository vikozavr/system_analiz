import json
import numpy as np

def process_graph(file_path):
    with open(file_path, "r") as file:
        content = json.load(file)
    
    vertices = content["nodes"]
    size = len(vertices)
    adjacency_matrix = np.zeros((size, size))
    
    for index in range(1, size + 1):
        neighbors = vertices[str(index)]
        for neighbor in neighbors:
            adjacency_matrix[index - 1][int(neighbor) - 1] = 1
    
    return adjacency_matrix