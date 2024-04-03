# Huffman Encoding Algorithm 

# Example input
input = 'hello world'

# STEP 1: Calculate the frequencies of characters
# Initialise a dictionary to store the frequency of characters
frequency = {}
# Iterate over each character in the input
for char in input:
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

# STEP 5: Output the generated Huffman dictionary
# Iterate each character and print in alphabetical order 
for char in sorted(codes):
    # Output each each character and its corresponding Huffman code
    print(char + '  ' + codes[char])

# STEP 6: Output the generated encoded word 
encodedInput = []
for char in input:
    if char != ' ':
        encodedInput.append(codes[char])
print(encodedInput)

def huffmanDecoder(encodedInput, codes):

    decodes = {}
    decodedOutput = []
    # Iterate through the items in the original dictionary
    for key, value in codes.items():
        # Swap the key and value and add to the reverse dictionary
        decodes[value] = key
    
    for char in sorted(decodes):
        # Output each each character and its corresponding Huffman code
        print(char + '  ' + decodes[char])

    for i in range(len(encodedInput)):
        decodedOutput.append(decodes[encodedInput[i]])

    print(decodedOutput)

huffmanDecoder(encodedInput, codes)