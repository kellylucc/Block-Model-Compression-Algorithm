import sys
import time
import timeit

# Initialise Variables
tagTableMap     = {}
outputList      = []
xyData          = []
xyzData         = []
curSrchTag      = ''
curSrchCoord    = []
curSrchTagCnt   = 1
outputList      = []
ySrch           = ['0','0','0','0','0','0','0']
yNext           = ['0','0','0','0','0','0','0']
curSrch         = ['0','0','0','0','0','0','0']
newSrch         = ['0','0','0','0','0','0','0']
xCount, yCount, zCount, xParent, yParent, zParent = 0,0,0,0,0,0

def getInputAndConvert():
    global xCount, yCount, zCount, xParent, yParent, zParent, tagTableMap
    counterToExit, counter  = 0, 0
    tagTableFound           = False
    xCounter,yCounter,zCounter = 0,0,0
    # Loop through each line of file
    while True:
        line = sys.stdin.readline()

        # Get data dimensions from first line
        if counter == 0:
            dimensionList = line.split(',')
            xCount, yCount, zCount, xParent, yParent, zParent = map(int, dimensionList)

        # Get the tag table details
        elif counter > 0 and tagTableFound == False:

            # Detect end of line and set a flag to start processing data
            if line == '\n':
                tagTableFound = True
                continue
            
            # Build a map using the tag/label inputs
            tagParts = line.strip().split(',')
            if len(tagParts) == 2:
                tag, label = tagParts
                tagTableMap[tag] = label.strip()
        
        # Get data and store in a seperate variable
        else:
            # Add to the 2d array when we dont have a blank line
            if line != '\n':            
                for xCounter, x in enumerate(line.strip()):
                    outputString = f"{xCounter},{yCounter},{zCounter},{1},{1},{1},{tagTableMap[x]} \n"
                    outputList.append(outputString)
                yCounter = yCounter + 1
            # If we have a blank line, append 2d array to the 3d array and clear the 2d array
            else:
                yCounter = 0
                zCounter = zCounter + 1
            # Increment counter to exit
            counterToExit = counterToExit + 1
            
            # If we reached the expected end of input file, exit
            if counterToExit > (yCount * zCount) + zCount - 1:
                break

        # Increment counter, which is used mainly for error logs
        counter = counter + 1

def compress1d2():
    outputListLen = len(outputList)
    for i, yLine in enumerate(outputList):
        if outputList[i] == 'x':
            continue
        
        found = 0
        # Loop through and find any lines we can match in 2d
        dimensionList = yLine.split(',')
        ySrch[0], ySrch[1], ySrch[2], ySrch[3], ySrch[4], ySrch[5], ySrch[6] = map(str, dimensionList)

        if int(ySrch[0]) != 0 and int(ySrch[0]) % xParent == xParent - 1:
            continue

        for j in range(i, outputListLen):
        # for j in range(i, outputListLen):
            nextSrchYLine = outputList[j]
            if outputList[j] == 'x':
                continue
            elif found > (xParent - 2):
                break
            elif (found + 1 + int(ySrch[0])) % xParent == 0:
                break
            newDimensionList = nextSrchYLine.split(',')
            yNext[0], yNext[1], yNext[2], yNext[3], yNext[4], yNext[5], yNext[6] = map(str, newDimensionList)

            if (int(yNext[0]) - int(ySrch[0])) > 4:
                break

            if (str(int(ySrch[0]) + 1 + found) == yNext[0] and
                ySrch[2]  == yNext[2]       and
                ySrch[3]  == yNext[3]       and
                ySrch[4]  == yNext[4]       and
                ySrch[5]  == yNext[5]       and
                ySrch[6]  == yNext[6]       and
                ySrch[1]  == yNext[1]):
                found = found + 1
                outputList[j] = 'x'
            else:
                continue
        
        if found > 0:
            # outputList[i] = ySrch[0] + ySrch[1] + ySrch[2] + ySrch[3] + str(int(ySrch[4]) + found) + ySrch[5] + ySrch[6]
            outputList[i] = f"{ySrch[0]},{ySrch[1]},{ySrch[2]},{str(int(ySrch[3]) + found)},{ySrch[4]},{ySrch[5]},{ySrch[6]}"

def compress2d():
    outputListLen = len(outputList)
    for i, yLine in enumerate(outputList):
        if outputList[i] == 'x':
            continue
        
        found = 0
        # Loop through and find any lines we can match in 2d
        dimensionList = yLine.split(',')
        ySrch[0], ySrch[1], ySrch[2], ySrch[3], ySrch[4], ySrch[5], ySrch[6] = map(str, dimensionList)

        if int(ySrch[1]) != 0 and int(ySrch[1]) % yParent == yParent - 1:
            continue

        for j in range(i+yCount, outputListLen, yCount):
        # for j in range(i, outputListLen):
            nextSrchYLine = outputList[j]
            if outputList[j] == 'x':
                continue
            elif found > (yParent - 2):
                break
            elif (found + 1 + int(ySrch[1])) % yParent == 0:
                break
            newDimensionList = nextSrchYLine.split(',')
            yNext[0], yNext[1], yNext[2], yNext[3], yNext[4], yNext[5], yNext[6] = map(str, newDimensionList)

            if (int(yNext[1]) - int(ySrch[1])) > 4:
                break

            if (str(int(ySrch[1]) + 1 + found) == yNext[1] and
                ySrch[2]  == yNext[2]       and
                ySrch[3]  == yNext[3]       and
                ySrch[4]  == yNext[4]       and
                ySrch[5]  == yNext[5]       and
                ySrch[6]  == yNext[6]       and
                ySrch[0]  == yNext[0]):
                found = found + 1
                outputList[j] = 'x'
            else:
                continue
        
        if found > 0:
            # outputList[i] = ySrch[0] + ySrch[1] + ySrch[2] + ySrch[3] + str(int(ySrch[4]) + found) + ySrch[5] + ySrch[6]
            outputList[i] = f"{ySrch[0]},{ySrch[1]},{ySrch[2]},{ySrch[3]},{str(int(ySrch[4]) + found)},{ySrch[5]},{ySrch[6]}"

def compress3d():
    outputListLen = len(outputList)
    for i, yLine in enumerate(outputList):
        if outputList[i] == 'x':
            continue
        
        found = 0
        
        # Loop through and find any lines we can match in 2d
        dimensionList = yLine.split(',')
        ySrch[0], ySrch[1], ySrch[2], ySrch[3], ySrch[4], ySrch[5], ySrch[6] = map(str, dimensionList)

        if int(ySrch[2]) != 0 and int(ySrch[2]) % zParent == zParent - 1:
            continue
    
        # if ySrch[0] == '12' and ySrch[1] == '25':
        #     print('here')
        for j in range(i+yCount*xCount, outputListLen, yCount*xCount):
        # for j in range(i, outputListLen):
            # j = j + 1
            nextSrchYLine = outputList[j]
            if outputList[j] == 'x':
                continue
            elif found > (zParent - 2):
                break
            elif (found + 1 + int(ySrch[2])) % zParent == 0:
                break
            newDimensionList = nextSrchYLine.split(',')
            yNext[0], yNext[1], yNext[2], yNext[3], yNext[4], yNext[5], yNext[6] = map(str, newDimensionList)

            if (int(yNext[2]) - int(ySrch[2])) > 4:
                break

            if (str(int(ySrch[2]) + 1 + found) == yNext[2] and
                ySrch[1]  == yNext[1]       and
                ySrch[3]  == yNext[3]       and
                ySrch[4]  == yNext[4]       and
                ySrch[5]  == yNext[5]       and
                ySrch[6]  == yNext[6]       and
                ySrch[0]  == yNext[0]):
                found = found + 1
                outputList[j] = 'x'
            else:
                continue
        
        if found > 0:
            outputList[i] = f"{ySrch[0]},{ySrch[1]},{ySrch[2]},{ySrch[3]},{ySrch[4]},{str(int(ySrch[5]) + found)},{ySrch[6]}"

def printOutput():
    # Loop through output list and print to console
    for outputLine in outputList:
        if outputLine != 'x':
            print(outputLine)

def saveToFile():
    outputFile = open("outputList.txt", "w")
    # Loop through output list and print to console
    for outputLine in outputList:
        if outputLine != 'x':
            outputFile.writelines(outputLine)

    outputFile.close()

def main():
    execution_time1 = timeit.timeit(getInputAndConvert, number=1)
    execution_time2 = timeit.timeit(compress1d2, number=1)
    execution_time3 = timeit.timeit(compress2d, number=1)
    execution_time4 = timeit.timeit(compress3d, number=1)
    execution_time5 = timeit.timeit(printOutput, number=1)
    
    print(f"Average execution time getInputAndConvert: {execution_time1:.6f} seconds")
    print(f"Average execution time compress1d2: {execution_time2:.6f} seconds")
    print(f"Average execution time compress2d: {execution_time3:.6f} seconds")
    print(f"Average execution time compress3d: {execution_time4:.6f} seconds")
    print(f"Average execution time printOutput: {execution_time5:.6f} seconds")

    # getInputAndConvert()
    # compress1d2()
    # compress2d()
    # compress3d()
    # printOutput()
    saveToFile()

if __name__ == "__main__":
    # startTime = time.process_time()
    
    main()

    # endTime = time.process_time()
    # print('Time taken in mseconds -', (endTime - startTime) * 1000)

# endTime = time.process_time()
# print('Time taken in mseconds -', (endTime - startTime) * 1000)