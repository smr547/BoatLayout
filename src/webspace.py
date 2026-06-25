#!/bin/env python3

import os
from urllib.parse import parse_qs
from spaces import Region, Space, Access, AccessType
import sys
import traceback

rootURL = "webspace.py"
spacesSoFar = []
nopath = False


def nameLink(space):
    # pathId = [str(s.id) for s in spacesSoFar]
    pathId = []
    for s in spacesSoFar:
        pathId.append(str(s.id))
        if s == space:
            break
    pathIds = ",".join(pathId)
    if nopath:
        return f'<a href="{rootURL}?space={space.id}&path=nopath">{space.name}</a>'
    else:
        return f'<a href="{rootURL}?space={space.id}&path={pathIds}">{space.name}</a>'

try:
    Region.loadCSV("./data/regions.csv")
    Space.loadCSV("./data/spaces.csv")
    Access.loadCSV("./data/accesses.csv")
except Exception as e:
    print(e)
    pass

def commonSpaces(listA, listB):
    common = []
    for space in listA:
        if space in listB:
            common.append(space)
    return common

# Parse the query string

# args = sys.argv[1].split("\\&")
# spaceId = args[0] 
# if len(args) > 1:
#     pathIds = args[1]
# else: 
#     pathIds = ""
# print("pathIds=",pathIds)
# if pathIds == "nopath":
#     pathIds = ""
#     nopath = True
# else:
#     nopath = False

# new parsing

qs = parse_qs(os.environ.get("QUERY_STRING", ""))

spaceId = int(qs.get("space", ["0"])[0])
#if spaceId is None:
if "space" not in os.environ.get("QUERY_STRING", ""):
    print("Status: 400 Bad Request")
    print("Content-Type: text/plain")
    print()
    print("Missing required query parameter: space")
    raise SystemExit




pathIds = qs.get("path", [""])[0]
if pathIds == "nopath":
    pathIds = ""
    nopath = True
else:
    nopath = False


for id in pathIds.split(','):
    try:
        id = int(id)
        if id in Space.spaces:
            spacesSoFar.append(Space.spaces[id])
            # print(f'pathId={id}')
    except:
        pass

openAccess = AccessType.findByName("Open")

try:
    # HTTP headers

    print("Content-type: text/html\n\n")

    # check that the space is known
    id = int(spaceId)
    if id in Space.spaces:
        space = Space.spaces[id]
        spacesSoFar.append(space)


        # Human passable accesses
        walkableAccesses = space.passableAccesses()
        if len(walkableAccesses) > 0:
            print(f'<h1>You are in {space.name} ({space.id})</h1>')
            print("You can move to: <br/><ul>")
            for wa in walkableAccesses:
                oSpace = wa.otherSpace(space)
                print("<li>", nameLink(oSpace)," (", oSpace.id, ")")
                if wa.accessType != openAccess:
                    print(f' via {wa.accessType.name}')
                print("</li>")
            print("</ul>")
        else:
            print("<h1>You have accessed ",space.name," (",space.id,")", "</h1>")

        # non human passable access
        nonWalkableAccesses = space.nonPassableAccesses()
        openAccesses = []
        coveredAccesses = []
        for nwa in nonWalkableAccesses:
            if nwa.accessType == openAccess:
                openAccesses.append(nwa)
            else:
                coveredAccesses.append(nwa)

        if len(openAccesses) > 0:
            print("You have open access to: <br/><ul>")
            for nwa in openAccesses:
                oSpace = nwa.otherSpace(space)
                print(f'<li>{nameLink(oSpace)} ({oSpace.id})</li>')
            print(f'</ul>')
        
        # covered accesses
        if len(coveredAccesses) > 0:
            print("You can access: <br/><ul>")
            for nwa in coveredAccesses:
                oSpace = nwa.otherSpace(space)
                print(f'<li>{nameLink(oSpace)} ({oSpace.id}) via {nwa.accessType.name}</li>')
            print(f'</ul>')

        # list path so far

        if not nopath:
            print(f'<p>Your path so far:</p><p>')
            path = []
            anchors = []

            for s in spacesSoFar:
                anchors.append(f'<a href="{rootURL}?space={s.id}&path={",".join(path)}">{s.name}</a>')
                path.append(str(s.id))
                if s == space:
                    break
            print(f'{" > ".join(anchors)}</p>')
    
    else:

        print(f'{spaceId} does not exist')
except Exception as e:
    print(f'Error: {e}')
    print(traceback.format_exc())
