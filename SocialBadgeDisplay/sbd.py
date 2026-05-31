"""
sbd.py - Social Badge Display

Created: March 7, 2026
@author: N. D. "Chip" Pearson (aka CmdrZin)
rev: 26may26 - port to laptop

"""

import os
import sys
from screeninfo import get_monitors
import pygame
import pygame.locals                    # get ALL locals
from badge import Badge                 # get the Badge class
import netdisplay as nd                 # get netdisplay class
Rect = pygame.Rect                      # redefine
import textdisplay as td                # get textdisplay class
import sbd_serial as ser                # get serial support
import hexnode as hn                    # get hex node support
import numbers
import json
from json import JSONEncoder

# *** SETUP SCREEN ***
# define display window
display_w = 900
display_h = 900
# get screen size
monitors = get_monitors()
screen_w = monitors[0].width
screen_h = monitors[0].height
# Set screen position of canvas..upper corner .. center
x = screen_w/2 - display_w/2
y = screen_h/2 - display_h/2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

# *** SETUP PYGAME ***
pygame.init()
# set up a simple canvas/screen to draw on
size = (display_w, display_h)
screen = pygame.display.set_mode(size)      # This creates a Surface to draw on
pygame.display.set_caption("SynShop Social Network")
# set up a timer for speed control
clock = pygame.time.Clock()
# Set up a Font for text
edit_font = pygame.font.Font('freesansbold.ttf', 20) # Name and size for ID & Name edit boxes
font = pygame.font.Font('freesansbold.ttf', 48) # Name and size

MAXID = 100                 # 469 maximum number of IDs supported for 1400x1400.

# *** LOCAL VARIABLES ***
BL_FILE = "BadgeList.json"
dt = 0                      # delta time for framerate independent rates.
rowCursor = 0               # select row to edit.
MAX_ROWS = 40
badgeCount = 0   # no used. Use len(badgeList)
#badgeList = {}             # Master Directory list maintained in Badges class.
nRadius = 99
centerCol = (int)((display_w) / (nRadius * 1.5))
centerCol += 1        # in cols
centerRow = (int)(((display_h/2) / nRadius) * 2)
centerRow += 0          # in rows
hexTable = hn.generateHexList(centerCol, centerRow, MAXID)     # returns a hex list.

# Set Net Display object and radius of nodes
nd = nd.netdisplay(screen, nRadius)

# set up Text Display area
td = td.textdisplay(screen)

# set up Node name edit boxes
id_rect = pygame.Rect(20, 700, 80, 24)
name_rect = pygame.Rect(110, 700, 80, 24)
color_active = pygame.Color("red")
color_passive = pygame.Color("green")
id_lable = edit_font.render("ID", True, (255,0,0))
name_lable = edit_font.render("NAME", True, (255,0,0))
id_lable_rect = pygame.Rect(20, 680, 80, 32)
name_lable_rect = pygame.Rect(110, 680, 80, 32)



#print("Col:" + str(centerCol) + " Row:" + str(centerRow))

# *** UTILITES ***
# Generate x,y based on Hex column and row
def getPosition(col, row):
    x = (int) (1.5 * col * nRadius / 2)
    y = (int) ((row * 0.86 * nRadius) / 2)
    y = y + 100
    return x,y

# Print all badges contacted
def dumpAll(bList):
    print("Dump All")
    for i,bg in bList.items():
        print( (str)(bg.id) )
        for b in bg.contactIdList:
            print("<-" + str(b))

# Generate a new Badge objcet
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
#        print(o.__dict__)
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
        f.close()

# Read in badgeList and call Badge(b.id,b) and addNode(b) for each Badge.
def restoreBadgeList():
    data = read_concatenated_json(BL_FILE)
    # add Badges to List and Nodes.
    for b in data:
        haveBadge = Badge.getBadge(b["id"])
        if haveBadge is not None:   # update existing badge
            haveBadge.setName(b["name"])
            haveBadge.setXY(b["x"], b["y"])
            for c in b["contactIdList"]:
                haveBadge.addContact(c)
                if Badge.getBadge(c) is None:
                    nb = newBadge(c, "CC");   # add contact as a new badge.
                    Badge.addBadge(nb)
        else:
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

badge = newBadge(0, "Base")
Badge.addBadge(badge)
nd.addNode(badge)
print(badge.name + " C:" + str(hexTable[badgeCount][0]) + " R:" + str(hexTable[badgeCount][1]))

textLine = "Social Contacts Network"
img = font.render(textLine, True, (255,0,0))
rect = img.get_rect()
rect.topleft = (150,20)
#cursor = Rect(rect.topright, (3,rect.height))

oneTime = True
row = 0

if fileCheck(BL_FILE):
    restoreBadgeList()



# Set up a simple process loop.
running = True
id_text = ""
name_text = ""
id_active = False
id_color = color_passive
name_color = color_passive
name_active = False
# Allow the user to end the game by closing the window.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # User clicked upper right winddow [X]
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if id_rect.collidepoint(event.pos):
                id_active = True                 # key strokes go to id box
                id_color = color_active
                id_text = ""
                name_text = ""
            else:
                id_active = False
                id_color = color_passive
            # trigger update on Event
            oneTime = True
                   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:  # remove last character
                if id_active:
                    id_text = id_text[:-1]
                elif name_active:
                    name_text = name_text[:-1]
            key_char = event.unicode
            if id_active:
                if key_char.isdigit():
                    if len(id_text) < 3:
                        id_text += key_char
            elif name_active:
                if key_char.isalnum():
                    if len(name_text) < 4:
                        name_text += key_char
            if event.key == pygame.K_RETURN and id_active:
                if id_text is not "":
                    tBadge = Badge.getBadge(int(id_text))
                    if tBadge is not None:
                        id_active = False
                        id_color = color_passive
                        name_active = True
                        name_color = color_active
            elif event.key == pygame.K_RETURN and name_active:
                tBadge = Badge.getBadge(int(id_text))
                if tBadge is not None:
                    name_active = False
                    name_color = color_passive
                    tBadge.setName(name_text)
                    saveBadgeList()
            if event.key == pygame.K_ESCAPE:
                id_active = False
                id_color = color_passive
                name_active = False
                name_color = color_passive
                id_text = ""
                name_text = ""
            # trigger update on Event
            oneTime = True

# """ TEST OPTIONS """
#    demoText = ser.readCom()       # Real Life
#    demoText = ser.readDemo()       # read test data .. generates NEW badges
    demoText = []                  # test only .. reads in json file


    if demoText:
#        print(demoText)
        tempList = []
        # Convert DUMP in int[]
        for n in demoText:
            nstr = n.decode('utf-8')   # to string
            if "*" not in nstr:
                tempList.append( (int(n,16)) )
#        print( tempList )
        oneTime = True
        # parse list
        # create a Badge object to test list of Badges
        if len(tempList) > 1:
            badge = newBadge(tempList[0], "XX")
#            Badge.addBadge(badge)       # adds only if NOT on list already
            # add contacts
        if len(tempList) > 2:       # new badges have only 2 elements in dump msg.
            for n in tempList[1:-1]:     # ignore last as it's the Badge ID
                badge.addContact(n)      # use ID as index to get Badge object later
                if Badge.getBadge(n) is None:
                    nb = newBadge(n, "CC");   # add contact as a new badge.
                    Badge.addBadge(nb)
        Badge.addBadge(badge)       # adds only if NOT on list already
        nd.addNode(badge)           # update Node display
 #       dumpAll(Badge.badgeList)
        saveBadgeList()

    if oneTime:
        oneTime = False
        screen.fill("linen")      # Clear drawing area
        screen.blit(img, rect)      # (source, location)
        nd.displayNet()
        td.showList(demoText)
        nd.displayLinks()
        # Draw Edit boxes
        pygame.draw.rect(screen, id_color, id_rect)
        pygame.draw.rect(screen, name_color, name_rect)
        id_surface = edit_font.render(id_text, True, (255,255,255))
        name_surface = edit_font.render(name_text, True, (255,255,255))
        screen.blit(id_surface, (id_rect.x+5, id_rect.y+5))
        screen.blit(name_surface, (name_rect.x+5, name_rect.y+5))
        screen.blit(id_lable, id_lable_rect)
        screen.blit(name_lable, name_lable_rect)
#        dumpAll(Badge.getBadgeList())
    
    pygame.display.flip()       # Refresh display
    
    # clock.tick() returns ...
    dt = clock.tick(30) / 1000  # limit frame rate to 30 FPS

# Shut Down and Exit
ser.close()
pygame.quit()
sys.exit()
