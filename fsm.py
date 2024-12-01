import time


FILE_FOLDER = 'hw10_data/'
ACCOUNT_FILE = 'account'
CARD_FILE = 'card'
ACCOUNT_TO_CARD_FILE = 'account_to_card'
ACCOUNT_TO_ACCOUNT_FILE = 'account_to_account'

def read_files(file_folder):
    start_time = time.time()
    vertex_dict = {}
    with open(file_folder + ACCOUNT_FILE, 'r') as f:
        for line in f:
            id, name, timestamp, black = line.strip().split(',')
            vertex_dict[int(id)] = name
    with open(file_folder + CARD_FILE, 'r') as f:
        for line in f:
            id, name, timestamp, black = line.strip().split(',')
            vertex_dict[int(id) + 800000] = name
    print('Read vertex list time:', time.time() - start_time)
            
    start_time = time.time()
    edge_list = []
    with open(file_folder + ACCOUNT_TO_CARD_FILE, 'r') as f:
        for line in f:
            account_id, card_id, timestamp, amt, strategy_name, trade_no, buscode, trade_flag, anticheat_prop_cluster, anticheat_prop_freq, anticheat_prop_relation, anticheat_prop_action, anticheat_prop_buyerseller = line.strip().split(',')
            edge_list.append((int(account_id), int(card_id) + 800000, (round(float(amt)), strategy_name, buscode)))
    with open(file_folder + ACCOUNT_TO_ACCOUNT_FILE, 'r') as f:
        for line in f:
            account_id1, account_id2, timestamp, amt, strategy_name, trade_no, buscode, trade_flag, anticheat_prop_cluster, anticheat_prop_freq, anticheat_prop_relation, anticheat_prop_action, anticheat_prop_buyerseller = line.strip().split(',')
            edge_list.append((int(account_id1), int(account_id2), (round(float(amt)), strategy_name, buscode)))
    print('Read edge list time:', time.time() - start_time)

    print('Vertex num:', len(vertex_dict))
    print('Edge num:', len(edge_list))

    start_time = time.time()
    edge_dict = {}
    for edge in edge_list:
        if edge[0] not in edge_dict:
            edge_dict[edge[0]] = {}
        if edge[1] not in edge_dict[edge[0]]:
            edge_dict[edge[0]][edge[1]] = [edge[2]]
        else:
            edge_dict[edge[0]][edge[1]].append(edge[2])

    reversed_edge_dict = {}
    for edge in edge_list:
        if edge[1] not in reversed_edge_dict:
            reversed_edge_dict[edge[1]] = {}
        if edge[0] not in reversed_edge_dict[edge[1]]:
            reversed_edge_dict[edge[1]][edge[0]] = [edge[2]]
        else:
            reversed_edge_dict[edge[1]][edge[0]].append(edge[2])
    print('Construct edge dict time:', time.time() - start_time)

    return vertex_dict, edge_dict, reversed_edge_dict

def get_triangle_topo(vertex_dict, edge_dict):
    triangle_topo_dict = dict()
    start_time = time.time()
    for i, vertex in enumerate(edge_dict):
        if i % 10000 == 0:
            print("Vertex:%d, Time:%f" % (i, time.time() - start_time))
            print("different triangle topo num:", len(triangle_topo_dict))
            for triangle_topo in triangle_topo_dict:
                if triangle_topo_dict[triangle_topo] > 5:
                    print(triangle_topo, triangle_topo_dict[triangle_topo])
        for neighbor1 in edge_dict[vertex]:
            if neighbor1 in edge_dict:
                for neighbor2 in edge_dict[neighbor1]:
                    if neighbor2 in edge_dict[vertex] and \
                            neighbor2 in edge_dict and vertex in edge_dict[neighbor2]:
                        for edge1 in edge_dict[vertex][neighbor1]:
                            for edge2 in edge_dict[neighbor1][neighbor2]:
                                for edge3 in edge_dict[neighbor2][vertex]:
                                    verify_set = (vertex_dict[vertex], vertex_dict[neighbor1], vertex_dict[neighbor2], edge1, edge2, edge3)
                                    if verify_set in triangle_topo_dict:
                                        triangle_topo_dict[verify_set] += 1
                                    else:
                                        triangle_topo_dict[verify_set] = 1
    return triangle_topo_dict

def get_homonymous_topo(vertex_dict, edge_dict):
    homonymous_topo_dict = dict()
    start_time = time.time()
    for i, vertex in enumerate(edge_dict):
        if i % 10000 == 0:
            print("Vertex:%d, Time:%f" % (i, time.time() - start_time))
            print("different homonymous topo num:", len(homonymous_topo_dict))
            for homonymous_topo in homonymous_topo_dict:
                if homonymous_topo_dict[homonymous_topo] > 5:
                    print(homonymous_topo, homonymous_topo_dict[homonymous_topo])
        for neighbor1 in edge_dict[vertex]:
            if neighbor1 in edge_dict:
                neighbor2_set = set(edge_dict[vertex].keys()) & set(edge_dict[neighbor1].keys())
                for neighbor2 in neighbor2_set:
                    for edge1 in edge_dict[vertex][neighbor1]:
                        for edge2 in edge_dict[neighbor1][neighbor2]:
                            for edge3 in edge_dict[vertex][neighbor2]:
                                verify_set = (vertex_dict[vertex], vertex_dict[neighbor1], vertex_dict[neighbor2], edge1, edge2, edge3)
                                if verify_set in homonymous_topo_dict:
                                    homonymous_topo_dict[verify_set] += 1
                                else:
                                    homonymous_topo_dict[verify_set] = 1
    return homonymous_topo_dict

def get_line_topo(vertex_dict, edge_dict):
    line_topo_dict = dict()
    start_time = time.time()
    for i, vertex in enumerate(edge_dict):
        if i % 10000 == 0:
            print("Vertex:%d, Time:%f" % (i, time.time() - start_time))
            print("different line topo num:", len(line_topo_dict))
        for neighbor1 in edge_dict[vertex]:
            if neighbor1 in edge_dict:
                for neighbor2 in edge_dict[neighbor1]:
                    if neighbor2 in edge_dict:
                        for neighbor3 in edge_dict[neighbor2]:
                            for edge1 in edge_dict[vertex][neighbor1]:
                                for edge2 in edge_dict[neighbor1][neighbor2]:
                                    for edge3 in edge_dict[neighbor2][neighbor3]:
                                        verify_set = (vertex_dict[vertex], vertex_dict[neighbor1], vertex_dict[neighbor2], vertex_dict[neighbor3], edge1, edge2, edge3)
                                        if verify_set in line_topo_dict:
                                            line_topo_dict[verify_set] += 1
                                        else:
                                            line_topo_dict[verify_set] = 1
    return line_topo_dict

def get_cycle_with_edge_topo(vertex_dict, edge_dict):
    cycle_with_edge_topo_dict = dict()
    start_time = time.time()
    for i, vertex in enumerate(edge_dict):
        if i % 10000 == 0:
            print("Vertex:%d, Time:%f" % (i, time.time() - start_time))
            print("different cycle with edge topo num:", len(cycle_with_edge_topo_dict))
        for neighbor1 in edge_dict[vertex]:
            if neighbor1 in edge_dict and vertex in edge_dict[neighbor1]:
                for neighbor2 in edge_dict[neighbor1]:
                    if neighbor2 is not vertex:
                        for edge1 in edge_dict[vertex][neighbor1]:
                            for edge2 in edge_dict[neighbor1][vertex]:
                                for edge3 in edge_dict[neighbor1][neighbor2]:
                                    verify_set = (vertex_dict[vertex], vertex_dict[neighbor1], vertex_dict[neighbor2], edge1, edge2, edge3)
                                    if verify_set in cycle_with_edge_topo_dict:
                                        cycle_with_edge_topo_dict[verify_set] += 1
                                    else:
                                        cycle_with_edge_topo_dict[verify_set] = 1
    return cycle_with_edge_topo_dict

def get_cycle_with_edge_in_topo(vertex_dict, edge_dict, reversed_edge_dict):
    cycle_with_edge_in_topo_dict = dict()
    start_time = time.time()
    for i, vertex in enumerate(edge_dict):
        if i % 10000 == 0:
            print("Vertex:%d, Time:%f" % (i, time.time() - start_time))
            print("different cycle with edge in topo num:", len(cycle_with_edge_in_topo_dict))
        for neighbor1 in edge_dict[vertex]:
            if neighbor1 in edge_dict and vertex in edge_dict[neighbor1]:
                for neighbor2 in reversed_edge_dict[neighbor1]:
                    if neighbor2 is not vertex:
                        for edge1 in edge_dict[vertex][neighbor1]:
                            for edge2 in edge_dict[neighbor1][vertex]:
                                for edge3 in edge_dict[neighbor2][neighbor1]:
                                    verify_set = (vertex_dict[vertex], vertex_dict[neighbor1], vertex_dict[neighbor2], edge1, edge2, edge3)
                                    if verify_set in cycle_with_edge_in_topo_dict:
                                        cycle_with_edge_in_topo_dict[verify_set] += 1
                                    else:
                                        cycle_with_edge_in_topo_dict[verify_set] = 1
    return cycle_with_edge_in_topo_dict

def main():
    vertex_dict, edge_dict, reversed_edge_dict = read_files(FILE_FOLDER)
    print(len(vertex_dict), len(edge_dict), len(reversed_edge_dict))
    # triangle_topo_dict = get_triangle_topo(vertex_dict, edge_dict)
    # homonymous_topo_dict = get_homonymous_topo(vertex_dict, edge_dict)
    
    line_topo_dict = get_line_topo(vertex_dict, edge_dict)
    print(len(line_topo_dict))
    with open('output/line_topo.txt', 'w') as f:
        for line_topo in line_topo_dict:
            if line_topo_dict[line_topo] >= 10000:
                f.write(str(line_topo) + ' ' + str(line_topo_dict[line_topo]) + '\n')

    cycle_with_edge_topo_dict = get_cycle_with_edge_topo(vertex_dict, edge_dict)
    print(len(cycle_with_edge_topo_dict))
    with open('output/cycle_with_edge_topo.txt', 'w') as f:
        for cycle_with_edge_topo in cycle_with_edge_topo_dict:
            if cycle_with_edge_topo_dict[cycle_with_edge_topo] >= 10000:
                f.write(str(cycle_with_edge_topo) + ' ' + str(cycle_with_edge_topo_dict[cycle_with_edge_topo]) + '\n')

    cycle_with_edge_in_topo_dict = get_cycle_with_edge_in_topo(vertex_dict, edge_dict, reversed_edge_dict)
    print(len(cycle_with_edge_in_topo_dict))
    with open('output/cycle_with_edge_in_topo.txt', 'w') as f:
        for cycle_with_edge_in_topo in cycle_with_edge_in_topo_dict:
            if cycle_with_edge_in_topo_dict[cycle_with_edge_in_topo] >= 10000:
                f.write(str(cycle_with_edge_in_topo) + ' ' + str(cycle_with_edge_in_topo_dict[cycle_with_edge_in_topo]) + '\n')

if __name__ == '__main__':
    main()