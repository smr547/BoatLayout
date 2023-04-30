import csv

class AccessType:
    types = {}
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
            print("An exception occured", e)
            return None

    @classmethod
    def loadCSV(cls, fileName):
        with open(fileName, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
            for row in reader:
                region = Region.newFromCSV(row)
                if region is not None:
                    print(region)

    def __init__(self, id, name):
        self.id = id
        self.name = name
        Region.regions[id] = self

    def __str__(self):
        return f'Region {self.id} -- {self.name}'
class Space:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        accesses = {}

class Access:
    def __init__(self, id, from_space, to_space, passable=False):
        self.id = id
        self.from_space = from_space
        self.to_space = to_space
        self.passable = passable


