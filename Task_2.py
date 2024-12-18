import sys
import os
from collections import deque
import random

class CacheSimulator:
    def __init__(self, cache_size, block_size, associativity, prefetch_size):
        """
        Initialize the cache simulator.

        :param cache_size: Total cache size in bytes.
        :param block_size: Block size in bytes.
        :param associativity: Associativity type (direct, assoc, assoc:n).
        :param prefetch_size: Number of blocks to prefetch on a miss.
        """
        self.cache_size = cache_size
        self.block_size = block_size
        self.prefetch_size = prefetch_size

        # Parse associativity
        if associativity == "direct":
            self.num_sets = cache_size // block_size
            self.associativity = 1
        elif associativity.startswith("assoc:"):
            self.associativity = int(associativity.split(":")[1])
            self.num_sets = (cache_size // block_size) // self.associativity
        elif associativity == "assoc":
            self.associativity = (cache_size // block_size)
            self.num_sets = 1
        else:
            raise ValueError("Invalid associativity type")

        # Initialize cache sets
        self.cache = [deque(maxlen=self.associativity) for _ in range(self.num_sets)]
        self.hits = 0
        self.misses = 0

    def access_memory(self, operation, address):
        """
        Simulate a memory access.

        :param operation: 'R' for read, 'W' for write.
        :param address: Memory address being accessed.
        """
        block_address = address // self.block_size
        set_index = block_address % self.num_sets
        tag = block_address // self.num_sets

        # Check if the block is in the cache
        set_ = self.cache[set_index]
        if tag in set_:
            self.hits += 1
        else:
            self.misses += 1
            if len(set_) == self.associativity:
                set_.popleft()  # FIFO replacement policy
            set_.append(tag)

            # Prefetch adjacent blocks
            for i in range(1, self.prefetch_size + 1):
                prefetch_address = block_address + i
                prefetch_tag = prefetch_address // self.num_sets
                prefetch_set_index = prefetch_address % self.num_sets
                prefetch_set = self.cache[prefetch_set_index]
                if prefetch_tag not in prefetch_set:
                    if len(prefetch_set) == self.associativity:
                        prefetch_set.popleft()
                    prefetch_set.append(prefetch_tag)

    def get_results(self):
        """
        Return the number of cache hits and misses.
        """
        return self.hits, self.misses

def generate_trace_file(filename, num_accesses):
    """
    Generate a memory trace file with random read/write operations.

    :param filename: Name of the trace file to generate.
    :param num_accesses: Number of memory accesses to generate.
    """
    with open(filename, 'w') as file:
        for _ in range(num_accesses):
            operation = random.choice(['R', 'W'])
            address = random.randint(0, 2**32 - 1)  # Generate a 32-bit memory address
            file.write(f"{operation} 0x{address:08x}\n")
        file.write("#eof\n")

def main():
    # Check arguments
    if len(sys.argv) != 6:
        print("Usage: ./cacheSimulator <cache size> <block size> <associativity> <prefetch size> <trace file>")
        return

    try:
        cache_size = int(sys.argv[1])
        block_size = int(sys.argv[2])
        associativity = sys.argv[3]
        prefetch_size = int(sys.argv[4])
        trace_file = sys.argv[5]

        # Validate inputs
        if cache_size & (cache_size - 1) != 0 or block_size & (block_size - 1) != 0:
            raise ValueError("Cache size and block size must be powers of 2.")

        if not os.path.exists(trace_file):
            raise FileNotFoundError(f"Trace file '{trace_file}' does not exist.")

        # Initialize the cache simulator
        simulator = CacheSimulator(cache_size, block_size, associativity, prefetch_size)

        # Read the trace file and simulate
        with open(trace_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line == "#eof":
                    break
                operation, address = line.split()
                address = int(address, 16)
                simulator.access_memory(operation, address)

        # Output results
        hits, misses = simulator.get_results()
        print(f"Cache Hits: {hits}")
        print(f"Cache Misses: {misses}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Uncomment the line below to generate a trace file before running the simulator.
    # generate_trace_file("memory_trace.txt", 1000)
    main()
