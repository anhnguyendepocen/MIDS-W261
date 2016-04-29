import re

def line_splitter(line):
    node, adj_list = re.split('\t',line.strip())
    node = node.strip('"')
    neighbors = eval(adj_list)
    node_list = []
    for neighbor in neighbors:
        node_list.append((node, neighbor))
    return node_list

with open("/Users/rcordell/Documents/MIDS/W261/week13/hw13/all-edges-out.txt",'w') as o:
    with open("/Users/rcordell/Documents/MIDS/W261/week09/HW9/data/wikipedia/all-pages-indexed-out.txt") as adjFile:
        for line in adjFile.readlines():
            for pair in line_splitter(line):
                 o.write('{0} {1}\n'.format(pair[0],pair[1]))

