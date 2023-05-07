#!/bin/env python3

from spaces import Region, Space, Access

try:
    Region.loadCSV("./data/regions.csv")
    Space.loadCSV("./data/spaces.csv")
    Access.loadCSV("./data/accesses.csv")
except Exception as e:
    print(e)

