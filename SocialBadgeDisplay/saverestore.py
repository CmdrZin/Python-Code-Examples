"""
saverestore.py - Social Badge recovery

Created: April 15, 2026
@author: N. D. "Chip" Pearson (aka CmdrZin)

Save the badgeList as a JSON file. Rename old and save new.
Recover the badgeList from a JSON file, if it exists.

Write badgeList out.
Read in badgeList and call Badge(b.id,b) and addNode(b) for each Badge.


"""

import os
import sys
import json
from json import JSONEncoder
from badge import Badge                 # get the Badge class

BL_FILE = "BadgeList.json"
hexTable = hn.generateHexList(centerCol, centerRow, MAXID)     # returns a hex list.

# *** UTILITES ***
# Generate x,y based on Hex column and row
def getPosition(col, row):
    x = (int) (1.5 * col * nRadius / 2)
    y = (int) ((row * 0.86 * nRadius) / 2)
    y += 50
    return x,y

def newBadge(bC, name = ""):
    b = Badge(bC)
    b.setName(name)
    x,y = getPosition(hexTable[bC][0],hexTable[bC][1] )
    b.setXY(x, y)
    return b

# Check if file exists
def fileCheck( fn ):
    if os.path.exists(fn):
        return open(fn)
    else:
        return None
    
# subclass
class BadgeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def read_concatenated_json(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    decoder = json.JSONDecoder()
    pos = 0
    objects = []
    
    while pos < len(content):
        # Skip potential whitespace between objects
        content = content.lstrip()
        if not content: break
        
        obj, index = decoder.raw_decode(content)
        objects.append(obj)
        content = content[index:].lstrip()
    return objects


def saveBadgeList():
    bl = Badge.getBadgeList()
    with open(BL_FILE, 'w') as f:
        for bg,badge in bl.items():     # get KEY and Object
            f.write(json.dumps(badge, indent=4, cls=BadgeEncoder) + '\n')   # write just the badge data

# Read in badgeList and call Badge(b.id,b) and addNode(b) for each Badge.
def restoreBadgeList():
    data = read_concatenated_json(BL_FILE)
    # add Badges to List and Nodes.
    for b in data:
        badge = Badge(b["id"])           # create Badge object
        badge.setName(b["name"])
        badge.setXY(b["x"], b["y"])
        for c in b["contactIdList"]:
            badge.addContact(c)
            if Badge.getBadge(c) is None:
                nb = newBadge(c, "CC");   # add contact as a new badge.
                Badge.addBadge(nb)
        Badge.addBadge(badge)       # adds only if NOT on list already
        nd.addNode(badge)           # update Node display
        print(badge)


# This is used to demo the module
def main():
    print("Look for " + BL_FILE)
    f = fileCheck(BL_FILE)
    if f:
        print("File exists.")
    else:
        print("Not found.")
        sys.exit()

    # from sbd.py
    b = Badge(0)
    b.setName("A")
    b.addContact(2)
    Badge.addBadge(b)
    b = Badge(1)
    b.setName("B")
    b.addContact(0)
    Badge.addBadge(b)
    b = Badge(2)
    b.setName("C")
    b.addContact(0)
    b.addContact(1)
    Badge.addBadge(b)

    bl = Badge.getBadgeList()
    print(bl)
   
    for bg,badge in bl.items():
        print("KEY:" + (str)(bg))
        print("  ID:" + (str)(badge.id) + "  Name:" + badge.name)
        for c in badge.contactIdList:
            print("  <-" + str(c))

    # Serialize into a string
    print(BadgeEncoder().encode(b))

    # Encode into JSON format string
    bJSONData = json.dumps(Badge.getBadge(2), indent=4, cls=BadgeEncoder)
    print(bJSONData)

    c = json.loads(bJSONData)       # c is a Dictionary.
    print(c["contactIdList"])       # so use this format.

    with open(BL_FILE, 'w') as f:
        for bg,badge in bl.items():     # get KEY and Object
            f.write(json.dumps(badge, indent=4, cls=BadgeEncoder) + '\n')   # write just the badge data

    data = read_concatenated_json(BL_FILE)

    for b in data:
        print(b)
    

if __name__ == "__main__":
    main()
