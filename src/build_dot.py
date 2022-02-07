#!/usr/bin/env python3
#
#
# Given two input CSV files:
# 
#  - Spaces CSV
#  - Access CSV
#
#
# Create a .dot file for Graphviz to build a diagram of the Yacht layout
#
#-------------------------------------------------
import argparse
import sys

def die(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(1)


parser = argparse.ArgumentParser(description='Create dot file from Spaces and Access CSV files')
parser.add_argument("-s", '--spaces', required=True, help='Path to Spaces.csv file')
parser.add_argument("-a", '--access', required=True, help='Path to Access.csv file')
parser.add_argument("-r", '--regions', required=True, help='Path to Regions.csv file')
parser.add_argument("-f", '--filter', required=False, default = None, help='Filter to a single region')

args = vars(parser.parse_args())

spaces = args['spaces']
access = args['access']
regions = args['regions']
filter = args['filter']


# build the regions dictionary

region = {}
with open(regions, 'r') as sf:
    for line in sf:
        fields = line.rstrip().split(",")
        id = fields[0]
        if id.upper() == "ID":
            continue
        name = fields[1]
        region[id] = name

# regions selected

if filter == None: 
    regions_selected = [r for r in region]
else:
    regions_selected = filter.split(',')

# build the space dictionary

space = {}
with open(spaces, 'r') as sf:
    for line in sf:
        fields = line.rstrip().split(",")
        id = fields[0]
        if id.upper() == "ID":
            continue
        name = fields[2] + "\n(" + id + ")"
        reg = fields[3]
        if reg not in region:
            die("Undefined region " + reg + " in space " + id)
        if name != "Name":
            space[id] = [name, reg]


# output dot file

print("digraph namadgi3 {")
print("  size=\"11.5,8\";")
print("  ratio=fill;")

for id in space:
    name = space[id][0]
    r = space[id][1]
    if r in regions_selected:
        line = "    S" + id + "  [label=\"" + name + "\"];"
        print(line)

print()

# print all accesses 

with open(access, 'r') as af:
    for line in af:
        fields = line.rstrip().split(",")
        id = fields[0]
        sFrom = fields[3]
        sTo = fields[4]
        name = fields[6]
        if id.upper() != "ID":
            if space[sFrom][1] in regions_selected and space[sTo][1] in regions_selected:
                line = "   S" + sFrom + " -> S" + sTo
                if fields[5] == "1":
                    line += " [dir=\"both\"]"
                line += ";"
                print(line)

# Define a subgraph for each region

for r in regions_selected:
    name = region[r]
    line = "   subgraph \"cluster_" + name +"\"  {label=\"" + name + "\"; "
    for s in space:
        if space[s][1] == r:
            line += "S" + s + "; "
    line += "}"
    print(line)


print("}");
