import ast
import re
import json

def parse_line(line):
    match = re.match(r"(.*)\s+(\d+)$", line.strip())
    if match:
        tuple_str = match.group(1)
        num_str = match.group(2)
        parsed_tuple = ast.literal_eval(tuple_str)

        # 解析出来的结果
        return parsed_tuple, int(num_str)
    else:
        print("Error: line format is not correct:", line)

def parse_topo_file(file_path):
    topos = []
    with open(file_path, 'r') as f:
        for line in f:
            topos.append(parse_line(line))
    return topos

def save_json_file(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def convert_to_list(topos, topo_type):
    output_list = []
    if topo_type == "line":
        for parsed_tuple, freq in topos:
            output = {"frequency": freq,
                        "nodes": [{"node_id": 0,
                                   "name": parsed_tuple[0]},
                                   {"node_id": 1,
                                    "name": parsed_tuple[1]},
                                    {"node_id": 2,
                                     "name": parsed_tuple[2]},
                                     {"node_id": 3,
                                      "name": parsed_tuple[3]}],
                        "edges": [{"source_node_id": 0,
                                      "target_node_id": 1,
                                      "amt": float(parsed_tuple[4][0]),
                                      "strategy_name": parsed_tuple[4][1],
                                      "buscode": parsed_tuple[4][2]},
                                        {"source_node_id": 1,
                                         "target_node_id": 2,
                                         "amt": float(parsed_tuple[5][0]),
                                         "strategy_name": parsed_tuple[5][1],
                                         "buscode": parsed_tuple[5][2]},
                                         {"source_node_id": 2,
                                            "target_node_id": 3,
                                            "amt": float(parsed_tuple[6][0]),
                                            "strategy_name": parsed_tuple[6][1],
                                            "buscode": parsed_tuple[6][2]}]}
            output_list.append(output)
    elif topo_type == "cycle_with_edge":
        for parsed_tuple, freq in topos:
            output = {"frequency": freq,
                        "nodes": [{"node_id": 0,
                                   "name": parsed_tuple[0]},
                                   {"node_id": 1,
                                    "name": parsed_tuple[1]},
                                    {"node_id": 2,
                                     "name": parsed_tuple[2]}],
                        "edges": [{"source_node_id": 0,
                                      "target_node_id": 1,
                                      "amt": float(parsed_tuple[3][0]),
                                      "strategy_name": parsed_tuple[3][1],
                                        "buscode": parsed_tuple[3][2]},
                                            {"source_node_id": 1,
                                             "target_node_id": 0,
                                             "amt": float(parsed_tuple[4][0]),
                                             "strategy_name": parsed_tuple[4][1],
                                             "buscode": parsed_tuple[4][2]},
                                             {"source_node_id": 1,
                                                "target_node_id": 2,
                                                "amt": float(parsed_tuple[5][0]),
                                                "strategy_name": parsed_tuple[5][1],
                                                "buscode": parsed_tuple[5][2]}]}
            output_list.append(output)
    elif topo_type == "cycle_with_edge_in":
        for parsed_tuple, freq in topos:
            output = {"frequency": freq,
                        "nodes": [{"node_id": 0,
                                   "name": parsed_tuple[0]},
                                   {"node_id": 1,
                                    "name": parsed_tuple[1]},
                                    {"node_id": 2,
                                     "name": parsed_tuple[2]}],
                        "edges": [{"source_node_id": 0,
                                      "target_node_id": 1,
                                      "amt": float(parsed_tuple[3][0]),
                                      "strategy_name": parsed_tuple[3][1],
                                        "buscode": parsed_tuple[3][2]},
                                            {"source_node_id": 1,
                                             "target_node_id": 0,
                                             "amt": float(parsed_tuple[4][0]),
                                             "strategy_name": parsed_tuple[4][1],
                                             "buscode": parsed_tuple[4][2]},
                                             {"source_node_id": 2,
                                                "target_node_id": 1,
                                                "amt": float(parsed_tuple[5][0]),
                                                "strategy_name": parsed_tuple[5][1],
                                                "buscode": parsed_tuple[5][2]}]}
            output_list.append(output)
    else:
        print("Error: topo_type is not correct.")
    return output_list

if __name__ == '__main__':
    cycle_with_edge_topo = parse_topo_file("output/cycle_with_edge_topo.txt")
    cycle_with_edge_in_topo = parse_topo_file("output/cycle_with_edge_in_topo.txt")
    line_topo = parse_topo_file("output/line_topo.txt")
    cwe_list = convert_to_list(cycle_with_edge_topo, "cycle_with_edge")
    cwei_list = convert_to_list(cycle_with_edge_in_topo, "cycle_with_edge_in")
    line_list = convert_to_list(line_topo, "line")
    save_json_file("bdci_data.json", cwe_list + cwei_list + line_list)
