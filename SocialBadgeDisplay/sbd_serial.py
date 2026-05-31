"""
sbd_serial.py - Serial port operations

Created: March 23, 2026
@author: N. D. "Chip" Pearson (aka CmdrZin)

"""

import serial
import serial.tools.list_ports

demoCount = 0
maxDemoCount = 9

# create an empty list
portList = []
# find all ports
ports = serial.tools.list_ports.comports()
# extract ports
for port in ports:
    portList.append(port.device)
# pick the first one. This could be changed to a test of all active ports.
if portList:
    print(portList)
    ser = serial.Serial(portList[0], 57600, timeout=5)
else:
    print("NO COM PORTS")
    ser = 0;

# read any data buffered in port. Will wait for \n or timeout.
# parse      b'*0002,0002*\n'
def readCom():
    if ser != 0:
        val = ser.in_waiting
        if val > 0:
            dataIn = ser.readline()
            if( dataIn[0] == ord('*') ):
                print("In:",dataIn)
                # Parse dump
                dumpList = []
                index = 1
                size = len(dataIn)
                while (index < size):
                    cid = dataIn[index:index+4]
                    dumpList.append(cid)
                    if dataIn[index+4] == ord('*'):
                        break;
                    index += 5
                return(dumpList)
        else:
            return []

# use BYTE format for data. b'0000'
def readDemo():
    global demoCount
    global maxDemoCount
    
    if demoCount > maxDemoCount:
        return []
    match demoCount:
        case 0:
            demoCount += 1
            return([b'0001',b'0001'])             # New badge
        case 1:
            demoCount += 1
            return([b'0002',b'0002'])             # New badge
        case 2:
            demoCount += 1
            return([b'0003',b'0003'])             # New badge
        case 3:
            demoCount += 1
            return([b'0001',b'0002',b'0003',b'0001'])  # contacts
        case 4:
            demoCount += 1
            return([b'0004',b'0004'])             # New badge
        case 5:
            demoCount += 1
            return([b'0004',b'0001',b'0002',b'0004'])  # contacts
        case 6:
            demoCount += 1
            return([b'0005',b'0005'])             # New badge
        case 7:
            demoCount += 1
            return([b'0006',b'0006'])             # New badge
        case 8:
            demoCount += 1
            return([b'0005',b'0001',b'0003',b'0005'])  # contacts
        case 9:
            demoCount += 1
            return([b'0007',b'0007'])             # New badge
        case 10:
            demoCount += 1
            return([b'0001',b'0004',b'0006',b'0001'])  # contacts
        case 11:
            demoCount += 1
            return([b'0008',b'0008'])             # New badge
        case 12:
            demoCount += 1
            return([b'0007',b'0001',b'0006',b'0008',b'0007'])  # contacts
        case _:
            return []

def close():
    if ser != 0:
        ser.close()
    
