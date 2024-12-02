import json
import numpy as np

def load_clusters_from_file(filepath):
    with open(filepath, 'r') as file:
        clusters = json.load(file)
    return [c if isinstance(c, list) else [c] for c in clusters]

def construct_matrix(clusters):
    n = sum(len(cluster) for cluster in clusters)
    matrix = np.ones((n, n), dtype=int)

    previously_seen_elements = set()
    for cluster in clusters:
        for element in cluster:
            element_index = element - 1
            matrix[element_index][list(previously_seen_elements)] = 0
        previously_seen_elements.update(cluster)
    
    return matrix

def identify_conflict_clusters(matrix):
    conflict_core = []
    n = len(matrix)
    
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i, j] == 0 and matrix[j, i] == 0:
                conflict_pair = sorted((i + 1, j + 1))
                if conflict_pair not in conflict_core:
                    conflict_core.append(conflict_pair)
                    
    return conflict_core

def main(file_path1, file_path2):
    clusters1 = load_clusters_from_file(file_path1)
    clusters2 = load_clusters_from_file(file_path2)
    
    matrix1 = construct_matrix(clusters1)
    matrix2 = construct_matrix(clusters2)

    matrix_and = np.multiply(matrix1, matrix2)

    matrix_or = np.maximum(matrix_and, np.transpose(matrix_and))

    conflict_clusters = identify_conflict_clusters(matrix_or)
    print(conflict_clusters)

