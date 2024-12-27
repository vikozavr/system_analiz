import json
import numpy as np


def parse_clusters(json_data):
    clusters = [cluster if isinstance(cluster, list) else [cluster] for cluster in json_data]
    total_elements = sum(len(cluster) for cluster in clusters)

    matrix = [[1] * total_elements for _ in range(total_elements)]
    preceding_elements = []

    for cluster in clusters:
        for earlier in preceding_elements:
            for current in cluster:
                matrix[current - 1][earlier - 1] = 0
        preceding_elements.extend(int(el) for el in cluster)

    return np.array(matrix)


def detect_conflict_core(matrix):
    conflict_core = []

    for row in range(len(matrix)):
        for col in range(row + 1, len(matrix)):
            if matrix[row][col] == 0 and matrix[col][row] == 0:
                pair = sorted([row + 1, col + 1])
                if pair not in conflict_core:
                    conflict_core.append(pair)

    return conflict_core


def main(json_ranking1, json_ranking2):
    ranking1 = json.loads(json_ranking1)
    ranking2 = json.loads(json_ranking2)

    matrix1 = parse_clusters(ranking1)
    matrix2 = parse_clusters(ranking2)

    combined_and = np.multiply(matrix1, matrix2)
    combined_and_transposed = np.multiply(matrix1.T, matrix2.T)
    final_matrix = np.maximum(combined_and, combined_and_transposed)

    conflict_core = detect_conflict_core(final_matrix)

    return json.dumps(conflict_core)
