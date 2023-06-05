#!/bin/env python3

from spaces import Region, Space, Access

try:
    Region.loadCSV("./data/regions.csv")
    Space.loadCSV("./data/spaces.csv")
    Access.loadCSV("./data/accesses.csv")
except Exception as e:
    # print(e)
    pass

# check that each space is mentioned in an access

for space in Space.spaces.values():
    if len(space.accesses) == 0:
        print(space)

