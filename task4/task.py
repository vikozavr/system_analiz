import numpy as np
from math import log2


def calculate_entropy(probabilities):
    entropy_value = 0
    for prob in probabilities:
        if prob > 0:
            entropy_value -= prob * log2(prob)
    return entropy_value


def main():
    joint_matrix = np.array([
        [20, 15, 10, 5],
        [30, 20, 15, 10],
        [25, 25, 20, 15],
        [20, 20, 25, 20],
        [15, 15, 30, 25]
    ])

    total_outcomes = joint_matrix.sum()
    joint_probabilities = joint_matrix / total_outcomes

    marginal_prob_A = joint_probabilities.sum(axis=1)
    marginal_prob_B = joint_probabilities.sum(axis=0)

    H_AB = calculate_entropy(joint_probabilities.flatten())
    H_A = calculate_entropy(marginal_prob_A)
    H_B = calculate_entropy(marginal_prob_B)

    mutual_info = H_A + H_B - H_AB

    print("Энтропия совместного события H(AB)", round(H_AB, 2))
    print("Количество информации I(A, B)", round(mutual_info, 2))
