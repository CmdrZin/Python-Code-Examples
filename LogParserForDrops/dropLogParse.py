###!/user/bin/env python
""" Top line for Unix systems. Comment out for Windows """

import os       # needed for file access.

import sys      # needed for sys functions.

lootTag = 'You have looted '
sellTag = 'll give you '
lootDB = {}     # blank dictionary.

def logParse(fname):
    'Parse a formatted log file'
    if os.path.exists(fname):
        fDL = open('DL_'+fname, 'w')
        print('Drop Log opened')

        flag = True
        
        'Read in each line'
        with open(fname, 'r', errors='ignore') as f:
            while flag:
                rline = f.readline()
                if rline == '':
                    break
                else:
                    # Find the channel string
                    L = lootTag in rline         # is loot tag?
                    S = sellTag in rline         # is sell tag?

                    # Write tagged line to the appropriate file
                    if L:
                        j = rline.find(lootTag)   # get index of tag
                        j += len(lootTag)
                        fDL.write(rline[j:])
                        # parse to database
                        k = rline.find(' ',j)     #skip over 1 or 2 char
                        l = rline.find('from',k)
                        # end may be ' or .
                        E = "'" in rline[j:]
                        #find the end
                        if E:
                            m = rline.find("'",j)
                        else:
                            m = rline.find(".",j)
                        key = rline[k+1:l-1]
                        a = dict(source=[rline[l+5:m]], sellTo='', buyFrom='')  #make source a list
                        # Check if key already exists. Check source list if it does, Add if not.
                        if not bool(lootDB):        # automatically add if empty.
                            lootDB[key] = a
                        elif key in lootDB:
                            # Check to see if a new source was found.
                            if a['source'][0] not in lootDB[key]['source']:
                                # then add it to the list.
                                lootDB[key]['source'].append(a['source'][0])
                        else:
                            # Add to database.
                            lootDB[key] = a
                    if S:
                        j = rline.find(sellTag)   # get index of tag
                        j += len(sellTag)
                        fDL.write(rline[j:])


        fDL.close()
        print('Drop Log closed')
    else:
        print("File '%s' not found." % fname)
        print("Usage: dropLogParse.py <filename>")


if __name__ == "__main__":
    # execute only if run as a script

    # Pass the second arg to the function. The first arg is the script name.
    logParse(sys.argv[1])

    # Print database
    for key in sorted(lootDB):
        for x in sorted(lootDB[key]['source']):
            print(key, ' ', x, ' ',lootDB[key]['sellTo'], ' ',lootDB[key]['buyFrom'])

    # Save to CSV file
    if os.path.exists(sys.argv[1]):
        fCSV = open('CSV_'+sys.argv[1], 'w')
        print('CSV file opened')

        for key in sorted(lootDB):
            d = len(lootDB[key]['source'])              # get the size of the list
            if d == 1:
                fCSV.write(key+','+lootDB[key]['source'][0]+','+lootDB[key]['sellTo']+','+lootDB[key]['buyFrom']+'\n')
            else:
                sl = '"'
                for x in sorted(lootDB[key]['source']):
                    sl += x+'\n'
                sl = sl[:-1]+'"'            # strip off last CR and add closing "
                fCSV.write(key+','+sl+','+lootDB[key]['sellTo']+','+lootDB[key]['buyFrom']+'\n')
                    
        fCSV.close()
        print('CSV file Log closed')
    else:
        print("File '%s' not found." % sys.argv[1])
        print("Usage: dropLogParse.py <filename>")
    
