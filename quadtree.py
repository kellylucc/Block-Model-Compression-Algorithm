import sys

# Open/Create output file
# outputFile = open("outputList.txt", "w")
# output2File = open("outputList2.txt", "w")

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
curSrchTag      = ''
curSrchCoord    = []
curSrchTagCnt   = 1
outputList      = []

# Testing variables
xSize           = 1
ySize           = 1
zSize           = 1
testLine        = ''
testingMode     = True

def saveToOutput():
    outputString = f"{curSrchCoord[0]},{curSrchCoord[1]},{curSrchCoord[2]},{curSrchTagCnt},{ySize},{zSize},{tagTableMap[curSrchTag]} \n"
    outputList.append(outputString)

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
if len(xyzData) != zCount:
    print ('z size does not match, current: ' + str(len(xyzData)) + ' expected: ' + str(zCount))
    quit()

##################################################################
# Call algorithm here, output should be in outputList variable

# appropriately divides data into smaller data for each quadrant
def build_quadrant_data(quadrant, data, length):
    
    # matching quadrant by identifying the bottom left corner as the start and the upper right corner as the right
    # quadrant 1 is upper left, 2 is upper right, 3 is lower left, 4 is lower right 
    match quadrant:
        case 1:
            x_start = 0
            y_start = length/2
            x_end = length/2
            y_end = length
        case 2:
            x_start = length/2
            y_start = length/2
            x_end = length
            y_end = length
        case 3:
            x_start = 0
            y_start = 0
            x_end = length/2
            y_end = length/2
        case 4:
            x_start = length/2
            y_start = 0
            x_end = length
            y_end = length/2

    # filling in quadrant_data with appropriate data taken from the original
    quadrant_data = []
    for y in range(int(y_start), int(y_end)):
        row_data = ""
        for x in range(int(x_start), int (x_end)):
            #with open("newnewoutput.txt", "a") as f:
            #    print(f"data[{y}][{x}]", file=f)
            row_data += data[y][x]
        quadrant_data.append(row_data)

    return quadrant_data

# checks if values inside a block are the same (by checking the first value against other values)
def check_equal_in_cube(data):
    first_tag = data[0][0]
   
    for row in data:
        for char in row:
            if char != first_tag:
                return False
    return True

# QuadtreeNode class to store associated values of each block
class QuadtreeBlock:
    def __init__(self, x, y, z, data):
        self.x = x
        self.y = y
        self.z = z
        self.xSize = 0
        self.ySize = 0
        self.zSize = 0
        self.data = data

# main driver code for processing data
def build_quadtree(x, y, z, data, length):
    
    # process one block at a time
    current_block = QuadtreeBlock(x, y, z, data)
    
    # get length of current block
    current_block.xSize = length
    current_block.ySize = length
    current_block.zSize = 1
    
    # recursively divide the block into quadrants until it either reaches 1*1*1 dimension
    # or when the block has all equal values AND is smaller than the parent block size
    if (((current_block.xSize <= xParent) and (current_block.ySize <= yParent) and (current_block.zSize <= zParent)) and (check_equal_in_cube(data))) or ((current_block.xSize == 1) and (current_block.ySize == 1) and (current_block.zSize == 1)):
        #with open("business.txt", "a") as f:
        print(f"{current_block.x},{64-current_block.y-current_block.ySize},{current_block.z},{current_block.xSize},{current_block.ySize},{current_block.zSize},{tagTableMap[data[0][0]]}")
    else:
        new_length = int(length/2)
        build_quadtree(current_block.x, current_block.y, current_block.z, build_quadrant_data(1, current_block.data, length), new_length)
        build_quadtree(current_block.x+new_length, current_block.y, current_block.z, build_quadrant_data(2, current_block.data, length), new_length)
        build_quadtree(current_block.x, current_block.y+new_length, current_block.z, build_quadrant_data(3, current_block.data, length), new_length)
        build_quadtree(current_block.x+new_length, current_block.y+new_length, current_block.z, build_quadrant_data(4, current_block.data, length), new_length)
    
# calling function with original data (starting at coordinates (0, 0, 0))
build_quadtree(0, 0, 0, xyzData[0], 64)
build_quadtree(0, 0, 1, xyzData[1], 64)
build_quadtree(0, 0, 2, xyzData[2], 64)
build_quadtree(0, 0, 3, xyzData[3], 64)
build_quadtree(0, 0, 4, xyzData[4], 64)
build_quadtree(0, 0, 5, xyzData[5], 64)
build_quadtree(0, 0, 6, xyzData[6], 64)
build_quadtree(0, 0, 7, xyzData[7], 64)

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