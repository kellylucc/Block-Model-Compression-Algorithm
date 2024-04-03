import sys
import time

# Open/Create output file
# outputFile = open("outputList.txt", "w")
# output2File = open("outputList2.txt", "w")

startTime = time.process_time()

# Initialise Variables
tagTableFound   = False
tagTableMap     = {}
outputList      = []
xData           = ''
xyData          = []
xyzData         = []
invertY         = False
counterToExit   = 0
counter         = 0
prevBlankLine   = False

# Testing variables
xSize           = 1
ySize           = 1
zSize           = 1
testLine        = ''
testingMode     = True

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
            # if len(xData) - 1 != xCount:
            #     print (xData)
            #     print ('x size does not match, current: ' + str(len(xData) - 1) + ' expected: ' + str(xCount) + ' counter: ' + str(counter))
            #     quit()
            
            xyData.append(line.strip())

        # If we have a blank line, append 2d array to the 3d array and clear the 2d array
        else:
            # Validate number of lines in each slice (y)
            # if len(xyData) != yCount:
            #     print ('y size does not match, current: ' + str(len(xyData)) + ' expected: ' + str(yCount) + ' counter: ' + str(counter))
            #     quit()

            # Reverse data for easier processing, as origin point is the bottom left instead of top left
            if invertY:
                xyzData.reverse()

            xyzData.append(xyData.copy())
            xyData.clear()
        
        # Increment counter to exit
        counterToExit = counterToExit + 1
        
        # If we reached the expected end of input file, exit
        if counterToExit > (yCount * zCount) + zCount - 1:
            break

    counter = counter + 1

# Validate number of slices (z)
# if len(xyzData) != zCount:
#     print ('z size does not match, current: ' + str(len(xyzData)) + ' expected: ' + str(zCount))
#     quit()

# Close input file
# inputFile.close()

##################################################################
# Call algorithm here, output should be in outputList variable

##################################################################


# if testingMode == False:
#     for outputLine in outputList:
#         print(outputLine)

##################################################################
# Testing code below
##################################################################
# if testingMode:
#     # Build output string and add to outputList
#     for zCounter, z in enumerate(xyzData):
#         for yCounter, y in enumerate(z):
#             for xCounter, x in enumerate(y):
#                 outputString = f"{xCounter},{yCounter},{zCounter},{xSize},{ySize},{zSize},{tagTableMap[x]} \n"
#                 print(outputString)
#                 #outputList.append(outputString)

#     # Sample output file for testing
#     for outputLine in outputList:
#         outputFile.writelines(outputLine)

#     outputFile.close()

#     for z in xyzData:
#         for y in z:
#             for x in y:
#                 testLine = testLine + x
#             output2File.write(testLine + "\n")
#             testLine = ''
#     output2File.close()

endTime = time.process_time()
print('Time taken in seconds -', (endTime - startTime) * 1000)
