#!/bin/env python3

from spaces import Region, Space, Access

try:
    Region.loadCSV("./data/regions.csv")
    Space.loadCSV("./data/spaces.csv")
    Access.loadCSV("./data/accesses.csv")
except Exception as e:
    print(e)


while (True):
    spaceId = input('Enter space number ')

    try:
        id = int(spaceId)
        if id in Space.spaces:
            print(Space.spaces[id].describe())
        else:
            print(f'{spaceId} does not exist')
    except Exception as e:
        print(f'Error: {e}')
