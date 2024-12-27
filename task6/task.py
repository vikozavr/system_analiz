import json
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import trapezoid


def create_interp_function(points):
    x = np.array([point[0] for point in points])
    y = np.array([point[1] for point in points])
    unique_x, index, counts = np.unique(x, return_index=True, return_counts=True)
    averaged_y = np.array([np.mean(y[i:i + c]) for i, c in zip(index, counts)])
    return interp1d(unique_x, averaged_y, kind='linear', fill_value="extrapolate")


def generate_membership_functions(sets):
    return {term["id"]: create_interp_function(term["points"]) for term in sets}


def calculate_membership_degrees(functions, value):
    return {term_id: functions[term_id](value) for term_id in functions}


def apply_fuzzy_rules(membership_degrees, rules):
    heating_membership = {}
    for temp_term, heating_term in rules:
        degree = min(membership_degrees.get(temp_term, 0), 1)
        heating_membership[heating_term] = max(heating_membership.get(heating_term, 0), degree)
    return heating_membership


def defuzzify(heating_membership, heating_functions, x_range):
    numerator = 0
    denominator = 0
    for term_id, degree in heating_membership.items():
        x = np.linspace(*x_range, 100)
        y = heating_functions[term_id](x)
        centroid = trapezoid(x * y, x) / trapezoid(y, x)
        numerator += centroid * degree
        denominator += degree
    return numerator / denominator if denominator != 0 else 0


def fuzzy_control(temperature_sets_json, heating_sets_json, rules_json, current_temperature):
    temperature_sets = json.loads(temperature_sets_json)["температура"]
    heating_sets = json.loads(heating_sets_json)["температура"]
    rules = json.loads(rules_json)

    temp_functions = generate_membership_functions(temperature_sets)
    heating_functions = generate_membership_functions(heating_sets)

    membership_degrees = calculate_membership_degrees(temp_functions, current_temperature)
    heating_membership = apply_fuzzy_rules(membership_degrees, rules)

    optimal_heating = defuzzify(heating_membership, heating_functions, (0, 26))
    return round(optimal_heating, 2)


if __name__ == "__main__":
    temperature_sets_json = """
    {
      "температура": [
          {
          "id": "холодно",
          "points": [
              [0,1],
              [18,1],
              [22,0],
              [50,0]
          ]
          },
          {
          "id": "комфортно",
          "points": [
              [18,0],
              [22,1],
              [24,1],
              [26,0]
          ]
          },
          {
          "id": "жарко",
          "points": [
              [24,0],
              [26,1],
              [50,1]
          ]
          }
      ]
    }
    """

    heating_sets_json = """
    {
      "температура": [
          {
            "id": "слабый",
            "points": [
                [0,0],
                [0,1],
                [5,1],
                [8,0]
            ]
          },
          {
            "id": "умеренный",
            "points": [
                [5,0],
                [8,1],
                [13,1],
                [16,0]
            ]
          },
          {
            "id": "интенсивный",
            "points": [
                [13,0],
                [18,1],
                [23,1],
                [26,0]
            ]
          }
      ]
    }
    """

    rules_json = """
    [
        ["холодно", "интенсивный"],
        ["комфортно", "умеренный"],
        ["жарко", "слабый"]
    ]
    """

    current_temp = 11

    optimal_heating = fuzzy_control(temperature_sets_json, heating_sets_json, rules_json, current_temp)
    print(f"Оптимальный уровень нагрева при температуре {current_temp}°C: {optimal_heating}")
