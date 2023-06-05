#!/bin/env python3

from spaces import Region, Space, Access, AccessType
import sys
import traceback

rootURL = "trilogy"
spacesSoFar = []


def nameLink(space):
    pathId = [str(s.id) for s in spacesSoFar]
    pathIds = ",".join(pathId)
    return f'<a href="{rootURL}?{space.id}&{pathIds}">{space.name}</a>'

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

args = sys.argv[1].split("\\&")
spaceId = args[0] 
if len(args) > 1:
    pathIds = args[1]
else: 
    pathIds = ""

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
    id = int(spaceId)
    if id in Space.spaces:
        space = Space.spaces[id]
        spacesSoFar.append(space)


        # Human passable accesses
        walkableAccesses = space.passableAccesses()
        if len(walkableAccesses) > 0:
            print(f'<h1>You are in {space.name} ({space.id})</h1>')
            print("go to: <br/><ul>")
            for wa in walkableAccesses:
                os = wa.otherSpace(space)
                print("<li>", nameLink(os)," (", os.id, ")")
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
                os = nwa.otherSpace(space)
                print(f'<li>{nameLink(os)} ({os.id})</li>')
            print(f'</ul>')
        
        # covered accesses
        if len(coveredAccesses) > 0:
            print("You can access: <br/><ul>")
            for nwa in coveredAccesses:
                os = nwa.otherSpace(space)
                print(f'<li>{nameLink(os)} ({os.id}) via {nwa.accessType.name}</li>')
            print(f'</ul>')

        # list path so far

        print(f'<p>Your path so far:</p><p>')
        path = []
        anchors = []

        for s in spacesSoFar:
            anchors.append(f'<a href="trilogy?{s.id}&{",".join(path)}">{s.name}</a>')
            path.append(str(s.id))
        print(f'{" > ".join(anchors)}</p>')
    
    else:

        print(f'{spaceId} does not exist')
except Exception as e:
    print(f'Error: {e}')
    print(traceback.format_exc())
