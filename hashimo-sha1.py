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

# Generate a set of all possible plaintext values
plaintexts = set(''.join(i) for i in itertools.product(char_set, repeat=plaintext_length))

# Initialize the table
table = {}
# Generate the chains
for i in range(num_chains):
    chain_start = plaintexts.pop() # use pop to remove plaintext from set
    chain_end = hashlib.sha1(chain_start.encode()).hexdigest()
    plaintext_start = chain_start # save plaintext for chain start
    plaintext_end = None # initialize plaintext for chain end
    for j in range(1, plaintext_length):
        chain_start = hashlib.sha1(chain_start.encode()).hexdigest()
        if chain_end not in table:
            plaintext_end = chain_start # save plaintext for chain end
            table[chain_end] = (plaintext_start, plaintext_end) # save plaintexts for chain start and end
            break
    if plaintext_end is None: # if chain was not completed, add plaintexts to set
        plaintexts.add(plaintext_start)

# Prompt the user to enter a filename to save the rainbow table
filename = input("Enter a filename to save the rainbow table: ")

# Save the table to the specified file in the desired format
with open(filename, "w") as f:
    for end, (start, plaintext) in table.items():
        f.write(f"{end}:{start}:{plaintext}\n")

def find_plaintext(password_hash, table):
    for i in range(plaintext_length):
        password = password_hash
        for j in range(i, plaintext_length):
            password = hashlib.sha1(password.encode()).hexdigest()
            if password in table:
                plaintext_start, plaintext_end = table[password]
                for k in range(j, plaintext_length):
                    password = hashlib.sha1(password.encode()).hexdigest()
                    if password == plaintext_end:
                        return plaintext_start, password_hash # Return both the plaintext and the hash
                break
    return None, None # Return None if the plaintext is not found

# Ask the user if they want to enter a custom password to be hashed
custom_choice = input("Do you want to hash a custom password? (y/n) ")
password_hash = None  # initialize password_hash variable

# If the user chooses not to enter a custom password, generate a random one and hash it
if custom_choice.lower() == "n":
    # Generate a random password
    password = ''.join(random.choices(char_set, k=plaintext_length))

    # Hash the password
    password_hash = hashlib.sha1(password.encode()).hexdigest()

    print(f"The randomly generated password is: {password}")
    print(f"The SHA-1 hash of the password is: {password_hash}")
elif custom_choice.lower() == "y":
    # Ask the user to enter a password to hash
    password = input("Enter a password to hash: ")

# Hash the password
password_hash = hashlib.sha1(password.encode()).hexdigest()

print(f"The SHA-1 hash of the password is: {password_hash}")

# Check if the password hash is in the rainbow table
if password_hash in table:
    plaintext, _hash = find_plaintext(password_hash, table) # Assign the plaintext and hash values
    if plaintext is not None:
        print(f"The password is: {plaintext}, Hash is: {_hash}")
    else:
        print("Unable to find the password in the rainbow table")
else:
    print("The password hash is not in the rainbow table.")
