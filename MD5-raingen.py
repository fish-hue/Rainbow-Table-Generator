import hashlib
import itertools

# Define parameters for the rainbow table
chain_length = 1000
num_chains = 10000

# Define the character set to use in the table
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-=[]{}|;':\",./<>?"

# Generate a list of plaintext values
plaintexts = [''.join(i) for i in itertools.product(charset, repeat=chain_length)]

# Initialize the table
table = {}

# Generate the chains
for i in range(num_chains):
    chain_start = plaintexts[i]
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
