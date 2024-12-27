import json
from math import log2

def make_node(parent, children):
    return {"parent": parent, "children": children}

def parse_data(parent, data, graph):
    keys = data.keys()
    for key in keys:
        children = data[key]
        node_children = parse_data(key, children, graph) if children else []
        graph[key] = make_node(parent, node_children)
    return list(keys)

def json_to_tree(json_string):
    graph = {}
    data = json.loads(json_string)
    parse_data(None, data, graph)
    return graph

def find_siblings(graph, key):
    parent = graph[key]["parent"]
    return [k for k, v in graph.items() if v["parent"] == parent and k != key]

def count_parents(key, graph):
    depth = 0
    while graph[key]["parent"]:
        key = graph[key]["parent"]
        depth += 1
    return depth

def count_indirect_children(graph, children, counter):
    for child in children:
        counter[0] += 1
        count_indirect_children(graph, graph[child]["children"], counter)

def analyze_relationships(graph):
    size = len(graph)
    results = [[0] * size for _ in range(5)]

    for key, attributes in graph.items():
        index = int(key) - 1
        
        if attributes["parent"]:
            results[0][index] = 1
        results[1][index] = len(attributes["children"])
        results[2][index] = count_parents(key, graph) - 1 if attributes["parent"] else 0
        
        counter = [0]
        count_indirect_children(graph, attributes["children"], counter)
        results[3][index] = counter[0]

        results[4][index] = len(find_siblings(graph, key))
    
    return results

def compute_entropy(matrix):
    num_columns = len(matrix[0])
    total_entropy = 0

    for column in zip(*matrix):
        column_entropy = -sum(
            (v / (num_columns - 1)) * log2(v / (num_columns - 1))
            for v in column if v > 0
        )
        total_entropy += column_entropy

    return total_entropy

def process_graph(input_data):
    graph_structure = {}
    parse_data(None, input_data, graph_structure)
    return graph_structure

def main(json_str):
    data = json.loads(json_str)
    graph = process_graph(data)
    relations = analyze_relationships(graph)
    entropy = compute_entropy(relations)
    print(f"Calculated Entropy: {entropy:.2f}")

test_structure = {
    "1": {
        "2": {
            "3": {
                "5": {},
                "6": {}
            },
            "4": {
                "7": {},
                "8": {}
            }
        }
    }
}

json_data = json.dumps(test_structure)
main(json_data)
