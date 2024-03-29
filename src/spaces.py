import csv

class AccessType:
    types = {}

    @classmethod
    def findByName(cls, name):
        for accessType in AccessType.types.values():
            if accessType.name == name:
                return accessType
        raise ValueError(f'Access type "{name}" not found')

    def __init__(self, id, name):
        self.id = id
        self.name = name
        AccessType.types[id] = self

# initialise AccessTypes

AccessType(1, "Open")
AccessType(2, "Doorway")
AccessType(3, "Buttoned door")
AccessType(4, "Door")
AccessType(5, "Hatch")
AccessType(6, "Drawer")
AccessType(7, "Seat hatch")
AccessType(8, "Under bunk hatch")
AccessType(9, "Backrest cushion")
AccessType(10, "Seat cushion")
AccessType(11, "Floor cover")
AccessType(12, "Seat Hatch")
AccessType(13, "fender step")
AccessType(14, "passerelle")
AccessType(15, "Shower screen")
AccessType(16, "Lifeline gate")

class Region:
    regions = {}

    @classmethod
    def newFromCSV(cls, row):
        try:
            id = int(row[0])
            name = row[1]
            region = Region(id, name)
            return region
        except Exception as e:
            # print("An exception occured", e)
            return None

    @classmethod
    def loadCSV(cls, fileName):
        with open(fileName, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
            for row in reader:
                region = Region.newFromCSV(row)
                # if region is not None:
                #     print(region)

    @classmethod
    def findByName(cls, name):
        for region in Region.regions.values():
            if region.name == name:
                return region
        return None

    def __init__(self, id, name):
        self.id = id
        self.name = name
        if Region.findByName(name) is not None:
            raise ValueError(f'Region {name} is duplicated')
        Region.regions[id] = self

    def __str__(self):
        return f'Region {self.id} -- {self.name}'

class Space:
    spaces = {}

    @classmethod
    def newFromCSV(cls, row):
        try:
            id = int(row[0])
            name = row[2]
            if len(name) == 0:
                return None
            regionId = int(row[3])
            space = Space(id, name, regionId)
            return space
        except Exception as e:
            # print("An exception occured", e)
            return None

    @classmethod
    def loadCSV(cls, fileName):
        with open(fileName, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
            for row in reader:
                space = Space.newFromCSV(row)
                # if space is not None:
                #     print(space)

    @classmethod
    def findByNameAndRegionId(cls, name, regionId):
        for space in Space.spaces.values():
            if space.name == name and space.region.id == regionId:
                return space
        return None

    def __init__(self, id, name, regionId):
        self.id = id
        self.name = name
        if regionId not in Region.regions:
            raise ValueError(f'Unknown Region id {regionId} for Space {id}: {name}')
        self.region = Region.regions[regionId]
        if Space.findByNameAndRegionId(name, regionId) is not None:
            raise ValueError(f'Space {name} is duplicated in {self.region}')
        Space.spaces[id] = self
        self.accesses = {}

    def addAccess(self, access):
        id = access.id
        if id in self.accesses:
            raise ValueError(f'{self.str()} alsready has Access {id} {access.name}')
        self.accesses[id] = access

    def passableAccesses(self):
        result = []
        for access in self.accesses.values():
            if access.passable:
                result.append(access)
        return result

    def nonPassableAccesses(self):
        result = []
        for access in self.accesses.values():
            if not access.passable:
                result.append(access)
        return result

    def describe(self):
        if self.region.name == self.name:
            desc = f'You are in {self.name} ({self.id})\r\n'
        else:
            desc = f'You are in {self.region.name} '
            desc += f'at {self.name} ({self.id})\r\n'
        desc += f'you can walk to '
        for access in self.accesses.values():
            if access.passable:
                space = access.otherSpace(self)
                desc += f'{space.name} ({space.id}), '
        
        reachableSpaces = []
        for access in self.accesses.values():
            if not access.passable:
                space = access.otherSpace(self)
                reachableSpaces.append(space)
        if len(reachableSpaces) > 0:
            desc +=f'\r\nyou can access '
            for spaces in reachableSpaces:
                desc += f'{space.name} ({space.id}), '

        return desc

    def __str__(self):
        return f'Space {self.id} -- {self.name}, {self.region}'


class Access:
    accesses = {}

    @classmethod
    def newFromCSV(cls, row):
        try:
            id = int(row[0])
            typeDesc = row[2]
            fromSpaceId = int(row[3])
            toSpaceId = int(row[4])
            p = int(row[5])
            passable = (p==1)

            accessType = AccessType.findByName(typeDesc)
            access = Access(id, accessType, fromSpaceId, toSpaceId, passable)
            return access
        except Exception as e:
            # print("An exception occured", e)
            return None

    @classmethod
    def loadCSV(cls, fileName):
        with open(fileName, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
            for row in reader:
                access = Access.newFromCSV(row)
                # if access is not None:
                #     print(access)

#    @classmethod
#    def findByName(cls, name):
#        for region in Region.regions.values():
#            if region.name == name:
#                return region
#
    def __init__(self, id, accessType, fromSpaceId, toSpaceId, passable=False):
        fromSpace = Space.spaces[fromSpaceId]
        toSpace = Space.spaces[toSpaceId]
        self.id = id
        self.accessType = accessType
        self.fromSpace = fromSpace
        self.toSpace = toSpace
        self.passable = passable

        fromSpace.addAccess(self)
        toSpace.addAccess(self)

        Access.accesses[id] = self

    def otherSpace(self, space):
        # given a space, describe the other accessible space

        if self.fromSpace == space:
            return self.toSpace
        else:
            return self.fromSpace


    def __str__(self):
        return f'Access {self.id} -- {self.accessType.name} from  {self.fromSpace} to {self.toSpace}'

