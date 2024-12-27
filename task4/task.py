import numpy as np
from math import log2

def calculate_entropy(prob_dist):
    return -sum(p * log2(p) for p in prob_dist if p > 0)

def main(matrix):
    total_elements = np.sum(matrix)
    joint_distribution = matrix / total_elements
    marginal_X = joint_distribution.sum(axis=1)
    marginal_Y = joint_distribution.sum(axis=0)

    joint_entropy = calculate_entropy(joint_distribution.flatten())
    entropy_X = calculate_entropy(marginal_X)
    entropy_Y = calculate_entropy(marginal_Y)

    mutual_information = entropy_X + entropy_Y - joint_entropy

    print(f"Количество информации I(X, Y): {mutual_information:.2f}")
    print(f"Энтропия совместного события H(XY): {joint_entropy:.2f}")

input_matrix = np.array([
    [20, 15, 10, 5],
    [30, 20, 15, 10],
    [25, 25, 20, 15],
    [20, 20, 25, 20],
    [15, 15, 30, 25]
])

main(input_matrix)
