import sys

tag_table_map = {
    "e": "NSW",
    "n": "NT",
    "q": "QLD",
    "s": "SA",
    "t": "TAS",
    "v": "VIC",
    "w": "WA",
    "o": "sea"
}

input_lines = []
x_coord_list, y_coord_list, z_coord_list, x_size_list, y_size_list, z_size_list, tag_list = ([] for i in range(7))

def read_input():
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            break
        input_lines.append(line)

    # Process all the input lines at once
    for line in input_lines:
        dimensionList = line.split(',')
        x_coord, y_coord, z_coord, x_size, y_size, z_size, tag = map(str, dimensionList)
        x_coord_list.append(x_coord)
        y_coord_list.append(y_coord)
        z_coord_list.append(z_coord)
        x_size_list.append(x_size)
        y_size_list.append(y_size)
        z_size_list.append(z_size)
        tag_list.append(tag)
        #print(f"{x_coord}, {y_coord}, {z_coord}, {x_size}, {y_size}, {z_size}, {tag}")

def find_initial_size():
    max_x_value = max(x_coord_list)
    max_y_value = max(y_coord_list)
    max_z_value = max(z_coord_list)
    largest_x_index = x_coord_list.index(max_x_value)
    largest_y_index = y_coord_list.index(max_y_value)
    largest_z_index = z_coord_list.index(max_z_value)
    original_x_size = int(max_x_value) + int(x_size_list[largest_x_index]) - int(min(x_coord_list))
    original_y_size = int(max_y_value) + int(y_size_list[largest_y_index]) - int(min(y_coord_list))
    original_z_size = int(max_z_value) + int(z_size_list[largest_z_index]) - int(min(z_coord_list))
    return (original_x_size, original_y_size, original_z_size)

def input_tags_into_map(x_coord, y_coord, z_coord, x_size, y_size, z_size, tag, min_x, min_y, min_z):
    x_coord -= min_x
    y_coord -= min_y
    z_coord -= min_z
    
    for k in range(z_size):
        for j in range(y_size):
            for i in range(x_size):
                initial_array_3d[z_coord+k][y_coord+j][x_coord+i] = list(tag_table_map.keys())[list(tag_table_map.values()).index(tag)]


read_input()
x, y, z = find_initial_size()

initial_row = []
for _ in range(x):
    initial_row.append([])

initial_array_3d = []
for i in range(z):
    initial_array_2d = [list(initial_row) for _ in range(x)]  # Create distinct inner lists
    initial_array_3d.append(initial_array_2d)

for i in range(len(x_coord_list)):
    input_tags_into_map(int(x_coord_list[i]), int(y_coord_list[i]), int(z_coord_list[i]), int(x_size_list[i]), int(y_size_list[i]), int(z_size_list[i]), tag_list[i], int(min(x_coord_list)), int(min(y_coord_list)), int(min(z_coord_list)))
 
for z_plane in reversed(initial_array_3d):
    for y_row in reversed(z_plane):
        print(''.join(y_row))
    print()