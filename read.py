import ast
import re

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

if __name__ == '__main__':
    topos = parse_topo_file("cycle_with_edge_topo.txt")
    print(len(topos), topos[0])
    topos = parse_topo_file("line_topo.txt")
    print(len(topos), topos[0])

