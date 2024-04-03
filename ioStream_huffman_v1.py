import sys

def encodeHuffman(codes, st, xCounter, xParent):

    # Count occurrences of current character
    global xCount
    global bound
    count = 1
    i = xCounter
    blockLim = xParent - (xCounter % xParent)
    length = len(st) - 1
    # length = bound
    eolCheck = count + xCounter
    # bound = xCount - 1
    encodedInput = []

    if eolCheck == bound:
        encodedInput.append(st[eolCheck])
        # print(len(encodedInput) + 1)
        return len(encodedInput) + 1, st[eolCheck]

    while (i < length and
            st[i] == st[i + 1] and 
            count < blockLim):
        
        encodedInput.append(codes[st[i]])

        # increment count of current character
        count += 1
            
        # Increment index while character is still the same
        i += 1
    
    # for char in st:
    #     if char != ' ':
    #         encodedInput.append(codes[char])
    # print(len(encodedInput) + 1)
    return len(encodedInput) + 1, st[i - 1]

def outputHuffman(codes, xyzData, tagTableMap, xParent):
    global xCount
    global length
    # outputListZ = []
    # outputListY = []
    length = len(xyzData[0][0]) - 1

    # iterate z axis using zCounter to keep track of position
    for zCounter, z in enumerate(xyzData):
        
        # iterate y axis using yCounter to keep track of position
        for yCounter, y in enumerate(z):
            
            # set xCounter to 0 everytime yCounter increments by 1
            xCounter = 0
            lineCounter = 0
            # while loop to check condition of xCounter compared to current line length before proceeding with RLE encoding
            while xCounter <= length:
                # run RLE encoding
                xSize, tag = encodeHuffman(codes, xyzData[zCounter][yCounter], xCounter, xParent)
                # define output string format
                outputString = f"{xCounter},{yCounter},{zCounter},{xSize},{ySize},{zSize},{tagTableMap[tag]} \n"
                # increment xCounter by the amount of counts returned by the encode function
                xCounter += xSize
                print(outputString)



def huffmanEncode(input):
    frequency = {}
    # Iterate over each character in the input
    for zCounter, z in enumerate(input):
        
        # iterate y axis using yCounter to keep track of position
        for yCounter, y in enumerate(z):
    
            for char in y:
                # Checks if not a space 
                if char != ' ':
                    # Checks if the character has appeared before, if so then increment by 1
                    if char in frequency:
                        frequency[char] += 1
                    # Otherwise assign it to 1
                    else:
                        frequency[char] = 1

    # STEP 2: Sort the characters according to frequency
    # Initialise a nodes list to store the character and its frequencies 
    nodes = []
    # Iterate over the char, freq key-value pair in dictionary
    for char, freq in frequency.items():
        # Adds the key-value tuple to nodes list in order to provide a starting point to Huffman tree
        nodes.append((freq, char))

    # A function to sort the tuples based on the first element of the tuple being frequency
    def sort(item):
        return item[0]

    # Sorts the list of nodes based on the frequency values as 
    # Ensures the lowest frequency characters are processed first for the Huffman tree
    nodes.sort(key=sort)

    # STEP 3: Build the Huffman tree 
    # Loop runs when there is at least two nodes in list, merges until one remains
    while len(nodes) > 1:
        # Remove the lowest frequency nodes from front of nodes list
        # char1 is first popped off as lowest frequency 
        frequency1, char1 = nodes.pop(0)
        # char2 is popped off after with the second-lowest frequency
        frequency2, char2 = nodes.pop(0)

        # Sum the frequencies of the two nodes 
        sum = frequency1 + frequency2
        # Create new node which is a tuple of the summed frequencies and the nodes
        newNode = (sum, (char1, char2))
        
        # Add the merged node back to the nodes list 
        nodes.append(newNode)
        # Sort list based on lowest frequency value for next iteration
        nodes.sort(key=sort)

    # Initialise the root node of Huffman tree where [1] accesses the characters
    huffmanTree = nodes[0][1]

    # STEP 4: Creat Huffman Codes 
    # Initialise a dictionary to store the codes 
    codes = {}

    # A recursive function to traverse the Huffman tree and create codes for each character
    def createCode(node, code=""):
        # Checks if the node is a string indicating its a leaf node 
        if isinstance(node, str):
            # Assign the code created to the dictionary 
            codes[node] = code
        # Otherwise gets the left and right child nodes indicating its an internal node
        else:
            # Left child is first element of merged node 
            leftNode = node[0]
            # Right child is second element of merged ndoe
            rightNode = node[1]
            # Append 0 if left child and 1 if right child to recursively build the codes
            createCode(leftNode, code + "0")
            createCode(rightNode, code + "1")
    # Traverse the tree to assign codes for each character in the codes dictionary
    createCode(huffmanTree)

    return codes

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
invertY         = False
counterToExit   = 0
counter         = 0
prevBlankLine   = False

# Testing variables
xSize           = 1
ySize           = 1
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

# Close input file
# inputFile.close()

##################################################################
# Call algorithm here, output should be in outputList variable

bound = xCount - 1

codes = huffmanEncode(xyzData)

outputHuffman(codes, xyzData, tagTableMap, xParent)

# outputRLE(xyzData, tagTableMap, xParent)
# outputList = outputRLE(xyzData, tagTableMap, xParent)

##################################################################
# if testingMode == False:
#     for outputLine in outputList:
#         print(outputLine)

##################################################################
# Testing code below

##################################################################
if testingMode:
    # Build output string and add to outputList
    for zCounter, z in enumerate(xyzData):
        for yCounter, y in enumerate(z):
            for xCounter, x in enumerate(y):
                outputString = f"{xCounter},{yCounter},{zCounter},{xSize},{ySize},{zSize},{tagTableMap[x]} \n"
                print(outputString)
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