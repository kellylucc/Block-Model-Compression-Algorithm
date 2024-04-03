import io

# Create a string to store the input
input_data = ""

while True:
    try:
        line = input()
    except EOFError:
        break

    # Append the line to the input data
    input_data += line

    # Check for an empty line to break the loop
    if line == "\n":
        break

# Create an input stream from the input data
input_stream = io.StringIO(input_data)

# Process the multiline input using a buffer
buffer_size = 1024
buffer = ""

while True:
    chunk = input_stream.read(buffer_size)
    if not chunk:
        break
    buffer += chunk

    # Check for an empty line in the buffer to process
    while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        # Process each line as needed
        line = line.strip()  # Remove leading and trailing whitespace
        print(f"Processed Line: {line}")

# Process any remaining content in the buffer
if buffer.strip():
    print(f"Processed Line: {buffer.strip()}")
