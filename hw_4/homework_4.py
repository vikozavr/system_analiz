import numpy as np
import math

def calculate_entropy(matrix):
    age_groups, types = matrix.shape

    total_sum = np.sum(matrix)

    probabilities = matrix / total_sum
    entropy_joint = -np.sum(probabilities * np.log2(probabilities, where=(probabilities > 0)))
    
    age_totals = np.sum(probabilities, axis=1)
    entropy_ages = -np.sum(age_totals * np.log2(age_totals, where=(age_totals > 0)))

    type_totals = np.sum(probabilities, axis=0)
    entropy_types = -np.sum(type_totals * np.log2(type_totals, where=(type_totals > 0)))

    conditional_probabilities = -np.where(probabilities > 0, probabilities * np.log2(probabilities), 0)
    entropy_conditional = np.sum(conditional_probabilities)

    entropy_difference = round(entropy_ages - entropy_conditional, 2)

    return np.round([
        entropy_joint,
        entropy_ages,
        entropy_types,
        entropy_conditional,
        entropy_difference
    ], 2)

def main():
    arr = np.array([
        [20, 15, 10, 5],
        [30, 20, 15, 10],
        [25, 25, 20, 15],
        [20, 20, 25, 20],
        [15, 15, 30, 25]
    ])
    result = calculate_entropy(arr)
    return result

