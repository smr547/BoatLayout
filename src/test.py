#!/bin/env python3

from spaces import Region, Space

try:
    Region.loadCSV("./data/regions.csv")
    Space.loadCSV("./data/spaces.csv")
except Exception as e:
    print(e)

