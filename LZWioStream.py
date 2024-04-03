import sys



# Open/Create output file
outputFile = open("outputList.txt", "w")
output2File = open("outputList2.txt", "w")

# Initialise Variables
tagTableFound   = False
tagTableMap     = {}
outputList      = []
xData           = ''
xyData          = []
xyzData         = []
counterToExit   = 0
counter         = 0
prevBlankLine   = False

# Testing variables
xSize           = 64
ySize           = 64
zSize           = 1
testLine        = ''
testingMode     = False

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
        # Remove leading/trailing spaces/end of line characters
        xData = line

        # Add to the 2d array when we dont have a blank line
        if line != '\n':

            # Validate number of characters in each line (x)
            if len(xData) - 1 != xCount:
                print (xData)
                print ('x size does not match, current: ' + str(len(xData) - 1) + ' expected: ' + str(xCount) + ' counter: ' + str(counter))
                quit()

            xyData.append(line.strip())

        # If we have a blank line, append 2d array to the 3d array and clear the 2d array
        else:
            # Validate number of lines in each slice (y)
            if len(xyData) != yCount:
                print ('y size does not match, current: ' + str(len(xyData)) + ' expected: ' + str(yCount) + ' counter: ' + str(counter))
                quit()

            xyzData.append(xyData.copy())
            xyData.clear()
        
        # Increment counter to exit
        counterToExit = counterToExit + 1
        
        # If we reached the expected end of input file, exit
        if counterToExit > (yCount * zCount) + zCount - 1:
            break

    counter = counter + 1

# Validate number of slices (z)
if len(xyzData) != zCount:
    print ('z size does not match, current: ' + str(len(xyzData)) + ' expected: ' + str(zCount))
    quit()

# Close input file
# inputFile.close()

##################################################################
# Call algorithm here, output should be in outputList variable

# Coordinate variables used for outputting
xCoord = 0

# Initialise stringMap to have each of the elements of the tag table as a key with an incrementing value as it's value
stringMap = {}
i = 0
for key in tagTableMap:
    stringMap[key] = i
    i = i + 1
mapIndex = i

# P is the first char in stream
P = xyzData[0][0][0]

# Loop through 3D Array
for z in range(zCount):
    
    
    for y in range(yCount):

        # xCoord starts at 0 at each new line
        xCoord = 0

        # x counter for the parent block size starts at 1 for each new line
        xBlock = 1

        for x in range(1, xCount):
            
            # C is the next char in the input stream
            C = xyzData[z][y][x]

            # If the xBlock size is equal to the max x parent block size, output current P and begin next block from C
            if xBlock == xParent:
                xBlock = 0
                # print(str(stringMap[P]) + " " + str(xCoord) + "," + str(y) + "," + str(zCoord) + "," + str(len(P)) + ",1,1," + tagTableMap[P[0]])
                # outputList = outputList + str(xCoord) + "," + str(y) + "," + str(zCoord) + "," + str(len(P)) + ",1,1," + tagTableMap[P[0]] + "\n"
                outputList.append(str(xCoord) + "," + str(y) + "," + str(z) + "," + str(len(P)) + ",1,1," + tagTableMap[P[0]])
                xCoord = xCoord + len(P)
                P = C
            else:

                # If x is at the end of the line, then we must print what we have and move to next line
                if x == xCount-1:

                    # If P + C is in the map already AND contain the same tag, then we can print P + C
                    if (P + C) in stringMap and P.find(C) != -1:
                        # print(str(stringMap[P + C]) + " " + str(xCoord) + "," + str(y) + "," + str(z) + "," + str(len(P + C)) + ",1,1," + tagTableMap[C])
                        # outputList = outputList + str(xCoord) + "," + str(y) + "," + str(z) + "," + str(len(P + C)) + ",1,1," + tagTableMap[C] + "\n"
                        outputList.append(str(xCoord) + "," + str(y) + "," + str(z) + "," + str(len(P + C)) + ",1,1," + tagTableMap[C])

                    # Else we must print them separately
                    else:
                        # If P and C contain the same tag, then we can add it the the map
                        if P.find(C) != -1:
                            stringMap[P + C] = mapIndex
                            mapIndex = mapIndex + 1
                    
                        # print(str(stringMap[P]) + " " + str(xCoord) + "," + str(y) + "," + str(z) + "," + str(len(P)) + ",1,1," + tagTableMap[P[0]])
                        # outputList = outputList + str(xCoord) + "," + str(y) + "," + str(z) + "," + str(len(P)) + ",1,1," + tagTableMap[P[0]] + "\n"
                        outputList.append(str(xCoord) + "," + str(y) + "," + str(z) + "," + str(len(P)) + ",1,1," + tagTableMap[P[0]])
                        
                        # xCoord gets moved to start of the next block
                        xCoord = xCoord + len(P)
                        # print(str(stringMap[C]) + " " + str(xCoord) + "," + str(y) + "," + str(z) + "," + str(len(C)) + ",1,1," + tagTableMap[C])
                        # outputList = outputList + str(xCoord) + "," + str(y) + "," + str(z) + "," + str(len(C)) + ",1,1," + tagTableMap[C] + "\n"
                        outputList.append(str(xCoord) + "," + str(y) + "," + str(z) + "," + str(len(C)) + ",1,1," + tagTableMap[C])
                        
                    # If x is at the end of the row and y is not at the end of the layer, we can set P to be the first char on the new line
                    if x == xCount-1 and y != yCount-1:
                        P = xyzData[z][y+1][0]
                    
                    # If y is at the end of the layer and z is not at the end of the input, we can set P to be the first char on the new layer
                    if y == yCount-1 and z != zCount-1:
                        P = xyzData[z+1][0][0]
                    
                    break
                
                # We get here if we are either not at the end of the xCount or yCount
                # If P + C is already in the map, then we concatenate P and C
                if (P + C) in stringMap:
                    P = P + C
                
                # Else, we print the current block and add the new block to the map
                else:
                    # print(str(stringMap[P]) + " " + str(xCoord) + "," + str(y) + "," + str(z) + "," + str(len(P)) + ",1,1," + tagTableMap[P[0]])
                    # outputList = outputList + str(xCoord) + "," + str(y) + "," + str(z) + "," + str(len(P)) + ",1,1," + tagTableMap[P[0]] + "\n"
                    outputList.append(str(xCoord) + "," + str(y) + "," + str(z) + "," + str(len(P)) + ",1,1," + tagTableMap[P[0]])
                    if P.find(C) != -1: 
                        stringMap[P + C] = mapIndex
                        mapIndex = mapIndex + 1
                    
                    # xCoord gets moved to start of the next block
                    xCoord = xCoord + len(P)
                    P = C
            # Increment the xBlock size
            xBlock = xBlock + 1

##################################################################
if testingMode == False:
    for outputLine in outputList:
        print(outputLine)

##################################################################
# Testing code below
##################################################################
if testingMode:
    # Build output string and add to outputList
    for zCounter, z in enumerate(xyzData):
        for yCounter, y in enumerate(z):
            for xCounter, x in enumerate(y):
                outputString = f"{xCounter},{yCounter},{zCounter},{xSize},{ySize},{zSize},{tagTableMap[x]} \n"
                # print(outputString)
                #outputList.append(outputString)

    # Sample output file for testing
    for outputLine in outputList:
        outputFile.writelines(outputLine)

    outputFile.close()

    for z in xyzData:
        for y in z:
            for x in y:
                testLine = testLine + x
            output2File.write(testLine + "\n")
            testLine = ''
    output2File.close()