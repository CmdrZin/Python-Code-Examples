"""
badge.py

Badge ID Class

March 7, 2026
@author: Nels D. "Chip" Pearson (aka CmdrZin)
ref: 11apr26
"""

# This ia the Badge class. It contines the ID and a list of contacts.
class Badge(dict):
    badgeList = {}          # Master Badge directory list.
    
    def __init__(self, id: int):
        dict.__init__(self, id = id, contactIdList = [], count = 0, x = 0, y = 0, name = "")

    # Add a badge to master list if NOT on the list already.
    def addBadge(badge):
        global badgeList
        if badge.id not in Badge.badgeList:
            Badge.badgeList[badge.id] = badge

    def getBadge(badge: int):
        global badgeList
        if badge in Badge.badgeList:
            return Badge.badgeList[badge]     # return Badge object
        else:
            return None

    def getBadgeList():
        return Badge.badgeList
    
    def getBadgeListLength():
        global badgeList
        return len(Badge.badgeList)

    # Add a contact badge ID if NOT on the list already.
    def addContact(self, badge: int):
        if badge not in self.contactIdList:
            self.contactIdList.append(badge)
            self.count += 1

    def setXY(self, X: int, Y: int):
        self.x = X
        self.y = Y

    def setName(self, s: str):
        self.name = s
        
# This is used to demo the Badge class
def main():
    # Create some Badges
    b1 = Badge(1234)
    b2 = Badge(2345)

    # Add some contacts
    b1.addContact(b2.id)
    b1.addContact(b2.id)
    b1.addContact(b2.id)
    b2.addContact(b1.id)
    b2.addContact(b1.id)

    # Badge object to main list
    Badge.addBadge(b1)
    Badge.addBadge(b2)
    
    # Print all badges contacted
    for i,bg in Badge.badgeList.items():
        print( (str)(i) )
        for b in bg.contactIdList:
            print("<-" + str(b))

if __name__ == "__main__":
    main()
