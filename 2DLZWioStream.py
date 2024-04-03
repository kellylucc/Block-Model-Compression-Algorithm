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

# Loop through 3D Array
for z in range(zCount):
    
    for y in range(0, yCount, 2):

        
        # xCoord starts at 0 at each new line
        xCoord = 0

        # x counter for the parent block size starts at 1 for each new line
        xBlock = 1

        for x in range(0, xCount, 2):
            
            
            # C0, C1, C2, C3 are the characters in the full parent block (hard coded for 2x2)
            C0 = xyzData[z][y][x]
            C1 = xyzData[z][y][x+1]
            C2 = xyzData[z][y+1][x]
            C3 = xyzData[z][y+1][x+1]

            # Case: 2x2 block
            if C0 == C1 and C0 == C2 and C0 == C3:
                outputList.append(str(x) + "," + str(y) + "," + str(z) + ",2,2,1," + tagTableMap[C0])

            # Case: 2x1 Block top half
            elif C0 == C1:
                outputList.append(str(x) + "," + str(y) + "," + str(z) + ",2,1,1," + tagTableMap[C0])

                # Case: 2x1 Block bottom half
                if C2 == C3:
                    outputList.append(str(x) + "," + str(y+1) + "," + str(z) + ",2,1,1," + tagTableMap[C2])
                # Case: bottom half not equal
                else:
                    outputList.append(str(x) + "," + str(y+1) + "," + str(z) + ",1,1,1," + tagTableMap[C2])
                    outputList.append(str(x+1) + "," + str(y+1) + "," + str(z) + ",1,1,1," + tagTableMap[C3])

            # Case: 2x1 Block bottom half
            elif C2 == C3:
                outputList.append(str(x) + "," + str(y+1) + "," + str(z) + ",2,1,1," + tagTableMap[C2])

                # Case: 2x1 Block top half
                if C0 == C1:
                    outputList.append(str(x) + "," + str(y) + "," + str(z) + ",2,1,1," + tagTableMap[C0])
                # Case: top half not equal
                else:
                    outputList.append(str(x) + "," + str(y) + "," + str(z) + ",1,1,1," + tagTableMap[C0])
                    outputList.append(str(x+1) + "," + str(y) + "," + str(z) + ",1,1,1," + tagTableMap[C1])

            # Case: 1x2 Block left half
            elif C0 == C2:
                outputList.append(str(x) + "," + str(y) + "," + str(z) + ",1,2,1," + tagTableMap[C0])

                # Case: 2x1 Block right half
                if C1 == C3:
                    outputList.append(str(x+1) + "," + str(y) + "," + str(z) + ",1,2,1," + tagTableMap[C1])

                # Case: right half not equal
                else:
                    outputList.append(str(x+1) + "," + str(y) + "," + str(z) + ",1,1,1," + tagTableMap[C1])
                    outputList.append(str(x+1) + "," + str(y+1) + "," + str(z) + ",1,1,1," + tagTableMap[C3])

            # Case: 1x2 Block right half
            elif C1 == C3:
                outputList.append(str(x+1) + "," + str(y) + "," + str(z) + ",1,2,1," + tagTableMap[C1])

                # Case: 2x1 Block left half
                if C0 == C2:
                    outputList.append(str(x) + "," + str(y) + "," + str(z) + ",1,2,1," + tagTableMap[C0])
                # Case: left half not equal
                else:
                    outputList.append(str(x) + "," + str(y) + "," + str(z) + ",1,1,1," + tagTableMap[C0])
                    outputList.append(str(x) + "," + str(y+1) + "," + str(z) + ",1,1,1," + tagTableMap[C2])

            # Case: no matches
            else:
                outputList.append(str(x) + "," + str(y) + "," + str(z) + ",1,1,1," + tagTableMap[C0])
                outputList.append(str(x+1) + "," + str(y) + "," + str(z) + ",1,1,1," + tagTableMap[C1])
                outputList.append(str(x) + "," + str(y+1) + "," + str(z) + ",1,1,1," + tagTableMap[C2])
                outputList.append(str(x+1) + "," + str(y+1) + "," + str(z) + ",1,1,1," + tagTableMap[C3])



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