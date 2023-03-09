import hashlib
import itertools
import random

# Define parameters for the rainbow table
num_chains = 100000

# Define the character sets to use for the plaintexts
char_sets = {
    "lowercase": "abcdefghijklmnopqrstuvwxyz",
    "uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "lowercase and uppercase combo": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "just digits": "0123456789",
    "lowercase and digits": "abcdefghijklmnopqrstuvwxyz0123456789",
    "uppercase and digits": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "lowercase, uppercase, and digit combo": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "just special": "!@#$%^&*()_+-=[]{}|;:,.<>?/~`",
    "just special and lowercase": "abcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[]{}|;:,.<>?/~`",
    "just special and uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[]{}|;:,.<>?/~`",
    "all": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
}

# Display the menu and ask user for the plaintext length and character set
print("Select a character set for the plaintexts:")
for i, (name, charset) in enumerate(char_sets.items()):
    print(f"{i+1}. {name}")

choice = int(input("Enter your choice: "))
char_set = char_sets[list(char_sets.keys())[choice-1]]

plaintext_length = int(input("Enter the desired length of plaintexts: "))

# Generate a list of all possible plaintext values
plaintexts = [''.join(i) for i in itertools.product(char_set, repeat=plaintext_length)]

# Initialize the table
table = {}
# Generate the chains
for i in range(num_chains):
    chain_start = plaintexts[i]
    chain_end = hashlib.md5(chain_start.encode()).hexdigest()
    plaintext = chain_start # save the plaintext for this chain
    for j in range(1, plaintext_length):
        chain_start = hashlib.md5(chain_start.encode()).hexdigest()
        chain_end = hashlib.md5(chain_end.encode()).hexdigest()
        if chain_end not in table:
            table[chain_end] = (chain_start, plaintext) # include plaintext value in output
            break
        plaintext = chain_start # update the plaintext value for the next step in the chain

# Prompt the user to enter a filename to save the rainbow table
filename = input("Enter a filename to save the rainbow table: ")

# Save the table to the specified file
with open(filename, "w") as f:
    for end, start in table.items():
        plaintext = start # set the plaintext to the start of the chain
        f.write(f"{end},{start},{plaintext}\n") # include plaintext value in output

def is_in_table(password_hash, table):
    if password_hash in table:
        return table[password_hash]
    return None

# Ask the user if they want to enter a custom password to be hashed
custom_choice = input("Do you want to hash a custom password? (y/n) ")
password_hash = None  # initialize password_hash variable

# If the user chooses not to enter a custom password, generate a random one and hash it
if custom_choice.lower() == "n":
    # Generate a random password
    password = ''.join(random.choices(char_set, k=plaintext_length))
else:
    # Ask the user to enter a password
    password = input("Enter the password to be hashed: ")

# Hash the password
password_hash = hashlib.md5(password.encode()).hexdigest()

# Check if the password hash is in the table
result = is_in_table(password_hash, table)

if result is not None:
    print(f"The password corresponding to hash {password_hash} is {result[1]}.")
else:
    print(f"The password corresponding to hash {password_hash} was not found in the table.")
