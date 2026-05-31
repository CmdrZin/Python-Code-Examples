"""
hexnode.py - Hex pattern generator

Created: April 2, 2026
@author: N. D. "Chip" Pearson (aka CmdrZin)

Generates the next Hex (col,row) for a spiral pattern

                 0,+2
         -1,+1     0     +1,+1
               5       1
                   X
               4       2
         -1,-1     3     +1,-1
                 0,-2
"""

# for directions 0:5
crAdj = [[0,-2],[1,-1],[1,1],[0,2],[-1,1],[-1,-1]]

# path. Move to Start, then n*dir except for last move which leaves you at Start.
path = [0, 4, 3, 2, 1, 0, 5]

# Fill-in box by looping around center. Adjusting hexCol & hexRow in a pattern.
# hexCol and hexRow are GLOBAL
def nextColRowHex(curHc, curHr):
    hexCol = curHc
    hexRow = curHr
    piDir = 0
    
    if piDir < 6:
        hexCol = hexCol + crAdj[ path[piDir] ][0]
        hexRow = hexRow + crAdj[ path[piDir] ][1]
    else:
        if piDir < 18:
            hexCol = hexCol + crAdj[ path[piDir % 6] ][0]
            hexRow = hexRow + crAdj[ path[piDir % 6] ][1]
            
    piDir += 1

# Starting at the center, spiral CCW in creasing circles of hexes up to maxID.
def generateHexList(centerC, centerR, maxID):
    hexCol = centerC
    hexRow = centerR
    dist = 1                # distance from center for path
    piDir = 0               # 0:Start..5:End
    pStep = 1               # number of steps to take in a direction
    mpStep = 1              # Maximum steps to take in a direction
    hexCR = []              # list of hex col/row indexed by ID.
    start = False

    hexCR.append([hexCol,hexRow])   # center hex
    
    for i in range(1,maxID):
        hexCol = hexCol + crAdj[ path[piDir] ][0]
        hexRow = hexRow + crAdj[ path[piDir] ][1]
        hexCR.append([hexCol,hexRow])
        pStep -= 1          # step taken
        if pStep == 0:      # done? yes..next direction unless at end
            if dist > 1:
                if piDir == 6 and start:    # last direction to take?
                    piDir = 0   # yes..reset for next circle
                    mpStep += 1 # increase the number of steps in each direction
                    hexCol = hexCol + crAdj[ 5 ][0]   # shift by 5 once
                    hexRow = hexRow + crAdj[ 5 ][1]
                    dist += 1
                    start = False
                else:           # no..next direction
                    start = True
                    piDir += 1          # next direction to move
            else:
                if piDir == 5 and start:    # last direction to take?
                    piDir = 0   # yes..reset for next circle
                    mpStep += 1 # increase the number of steps in each direction
                    hexCol = hexCol + crAdj[ 5 ][0]   # shift by 5 once
                    hexRow = hexRow + crAdj[ 5 ][1]
                    dist += 1
                    start = False
                else:           # no..next direction
                    start = True
                    piDir += 1          # next direction to move
            pStep = mpStep  # reset the number of steps to take.
        if not start:
            pStep = 1
        if piDir == 6 and pStep == 2:   # one less at the end of the path.
            pStep = 1
        # no..repeat step.                

    return hexCR
