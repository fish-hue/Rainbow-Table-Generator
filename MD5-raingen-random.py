import hashlib
import random

# Define parameters for the rainbow table change as needed
chain_length = 1000
num_chains = 10000

# Generate a list of random plaintext values
plaintexts = [str(random.randint(0, 10**8)) for i in range(num_chains * chain_length)]

# Initialize the table
table = {}

# Generate the chains
for i in range(num_chains):
    chain_start = plaintexts[i * chain_length]
    chain_end = hashlib.md5(chain_start.encode()).hexdigest()
    for j in range(1, chain_length):
        chain_start = hashlib.md5(chain_start.encode()).hexdigest()
        chain_end = hashlib.md5(chain_end.encode()).hexdigest()
        if chain_end not in table:
            table[chain_end] = chain_start

# Save the table to a file
with open("rainbow_table.txt", "w") as f:
    for end, start in table.items():
        f.write(f"{end}:{start}\n")
