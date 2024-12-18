import random

def generate_sequential_trace(filename, num_accesses, block_size=4):
    """
    #Generate a sequential memory trace file.

    :param filename: Name of the trace file to generate.
    :param num_accesses: Number of memory accesses to generate.
    :param block_size: Increment between sequential addresses (default: 4 bytes).
    """
    with open(filename, 'w') as file:
        address = 0  # Start at address 0
        for _ in range(num_accesses):
            operation = random.choice(['R', 'W'])  # Randomly choose between 'R' and 'W'
            file.write(f"{operation} 0x{address:08x}\n")
            address += block_size  # Sequentially increment address by block size
        file.write("#eof\n")
    print(f"Sequential trace file '{filename}' generated with {num_accesses} accesses.")

def generate_mixed_trace(filename, num_accesses):
    """
    #Generate a mixed memory trace file with sequential and random accesses.

    :param filename: Name of the trace file to generate.
    :param num_accesses: Number of memory accesses to generate.
    """
    with open(filename, 'w') as file:
        for i in range(num_accesses):
            operation = random.choice(['R', 'W'])  # Randomly choose between 'R' and 'W'
            # Alternate between sequential and random access
            if i % 2 == 0:
                address = i * 4  # Sequential access
            else:
                address = random.randint(0, 2**32 - 1)  # Random access
            file.write(f"{operation} 0x{address:08x}\n")
        file.write("#eof\n")
    print(f"Mixed trace file '{filename}' generated with {num_accesses} accesses.")

if __name__ == "__main__":
    print("1. Generate Sequential Trace")
    print("2. Generate Mixed Trace")
    choice = input("Enter your choice (1 or 2): ")

    try:
        if choice not in ['1', '2']:
            print("Invalid choice! Please enter 1 or 2.")
            exit(1)

        num_accesses = int(input("Enter the number of memory accesses to generate: "))
        if num_accesses <= 0:
            print("Number of accesses must be greater than 0!")
            exit(1)

        if choice == '1':
            filename = input("Enter the filename for the sequential trace: ")
            block_size = int(input("Enter the block size (default 4 bytes): ") or 4)
            generate_sequential_trace(filename, num_accesses, block_size)
        elif choice == '2':
            filename = input("Enter the filename for the mixed trace: ")
            generate_mixed_trace(filename, num_accesses)

    except ValueError as e:
        print(f"Error: {e}. Please enter valid inputs.")
