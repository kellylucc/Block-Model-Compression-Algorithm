import sys

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
def build_sub_cube_data(octant, data, size):
    match octant:
        case 1:
            x_start = 0
            y_start = size/2
            z_start = 0
            x_end = size/2
            y_end = size
            z_end = size/2
        case 2:
            x_start = size/2
            y_start = size/2
            z_start = 0
            x_end = size
            y_end = size
            z_end = size/2
        case 3:
            x_start = 0
            y_start = 0
            z_start = 0
            x_end = size/2
            y_end = size/2
            z_end = size/2
        case 4:
            x_start = size/2
            y_start = 0
            z_start = 0
            x_end = size
            y_end = size/2
            z_end = size/2
        case 5:
            x_start = 0
            y_start = size/2
            z_start = size/2
            x_end = size/2
            y_end = size
            z_end = size
        case 6:
            x_start = size/2
            y_start = size/2
            z_start = size/2
            x_end = size
            y_end = size
            z_end = size
        case 7:
            x_start = 0
            y_start = 0
            z_start = size/2
            x_end = size/2
            y_end = size/2
            z_end = size
        case 8:
            x_start = size/2
            y_start = 0
            z_start = size/2
            x_end = size
            y_end = size/2
            z_end = size
    
    sub_cube_data = []
    for z in range(int(z_start), int(z_end)):
        slice_data = []
        for y in range(int(y_start), int(y_end)):
            row_data = ""
            for x in range(int(x_start), int(x_end)):
                row_data += data[z][y][x]
            slice_data.append(row_data)
        sub_cube_data.append(slice_data)

    return sub_cube_data

def check_equal_in_cube(data):
    first_character = data[0][0]
    
    for row in data:
        for char in row:
            if char != first_character:
                return False
    return True

class OctreeNode:
    def __init__(self, x, y, z, size, data):
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.data = data
            
def build_octree(x, y, z, size, data):
    current_node = OctreeNode(x, y, z, size, data)
    
    if (size > 1):
        if check_equal_in_cube(data) == False:
            # print("new cube")
            new_size = int(size/2)
            build_octree(x, y, z, new_size, build_sub_cube_data(1, data, size))
            build_octree(x+new_size, y, z, new_size, build_sub_cube_data(2, data, size))
            build_octree(x, y+new_size, z, new_size, build_sub_cube_data(3, data, size))
            build_octree(x+new_size, y+new_size, z, new_size, build_sub_cube_data(4, data, size))
            build_octree(x, y, z+new_size, new_size, build_sub_cube_data(5, data, size))
            build_octree(x+new_size, y, z+new_size, new_size, build_sub_cube_data(6, data, size))
            build_octree(x, y+new_size, z+new_size, new_size, build_sub_cube_data(7, data, size))
            build_octree(x+new_size, y+new_size, z+new_size, new_size, build_sub_cube_data(8, data, size))
        else:
            print(f"{current_node.x},{current_node.y},{current_node.z},{current_node.size},{current_node.size},{current_node.size},{tagTableMap[current_node.data[0][0][0]]}")
            # print(current_node.data, end="")
    else:
        print(f"{current_node.x},{current_node.y},{current_node.z},{current_node.size},{current_node.size},{current_node.size},{tagTableMap[current_node.data[0][0][0]]}")
        # print(current_node.data, end="")

build_octree(xCount, yCount, zCount, xParent, xyzData)
##################################################################