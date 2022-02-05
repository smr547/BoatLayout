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

parser = argparse.ArgumentParser(description='Create dot file from Spaces and Access CSV files')
parser.add_argument("-s", '--spaces', required=True, help='Path to Spaces.csv file')
parser.add_argument("-a", '--access', required=True, help='Path to Access.csv file')

args = vars(parser.parse_args())

spaces = args['spaces']
access = args['access']

# build the space dictionary

space = {}
with open(spaces, 'r') as sf:
    for line in sf:
        fields = line.split(",")
        id = fields[0]
        name = fields[2]
        if name != "Name":
            space[id] = name


# output dot file

print("digraph namadgi3 {")
for id in space:
    name = space[id]
    line = "    S" + id + "  [label=\"" + name + "\"];"
    print(line)

print()

with open(access, 'r') as af:
    for line in af:
        fields = line.split(",")
        id = fields[0]
        sFrom = fields[3]
        sTo = fields[4]
        name = fields[6]
        if id != "Id":
            line = "   S" + sFrom + " -> S" + sTo
            if fields[5] == "1":
                line += " [dir=\"both\"]"
            line += ";"
            print(line)


print("}");
