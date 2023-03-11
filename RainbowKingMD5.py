import requests
import re
import hashlib

# Define the hash type we want to look for
HASH_TYPE = 'MD5'

# Function to crawl website and collect hashes
def crawl_website(url):
    response = requests.get(url)
    hashes = set()
    hash_pattern = r"\b[A-Fa-f0-9]{32}\b"  # Use regex to match MD5 hashes
    matches = re.findall(hash_pattern, response.text)
    if matches:
        for match in matches:
            hash_object = hashlib.new(HASH_TYPE.lower())
            hash_object.update(match.encode('utf-8'))
            hash_value = hash_object.hexdigest()
            hashes.add(hash_value)
    return hashes

# Function to sort hashes into a separate file
def sort_hashes(hashes, filename):
    with open(filename, "w") as f:
        for hash_value in hashes:
            f.write(f"{hash_value}\n")

# Function to check the hashes against the table
def check_hashes(filename, table, verbose=False):
    with open(filename, "r") as f:
        for line in f:
            hash_value = line.strip()
            start_hash = hash_value
            for i in range(8):
                start_hash = hashlib.md5(start_hash.encode()).hexdigest()
                if start_hash in table:
                    if verbose:
                        print(f"Plaintext found for hash {hash_value}: {table[start_hash][1]}")
                    else:
                        print(f"Plaintext found for hash {hash_value}.")
                    break
            else:
                if verbose:
                    print(f"No plaintext found for hash {hash_value}.")
                else:
                    print(f"No plaintext found for hash {hash_value}.")

# Function to create the rainbow table
def create_rainbow_table():
    import string

    # Prompt user for custom parameters or use default
    default = input("Would you like to use the default parameters? Default password length is 10 characters, 1 million chains with a chain length of 20,000 (y/n): ")
    if default.lower() == 'y':
        charset = 'all'
        length = 10
        num_chains = 1000000
        chain_length = 20000
        filename = input("Enter the name of the file to save the table: ")
    else:
        charset = input("Enter the character set to use (lowercase/uppercase/digits/special/all): ")
        length = int(input("Enter the length of passwords to generate: "))
        num_chains = int(input("Enter the number of chains to generate: "))
        chain_length = int(input("Enter the length of each chain: "))
        filename = input("Enter the name of the file to save the table: ")

    # Generate table
    table = {}
    for i in range(num_chains):
        password = generate_password(charset, length)
        chain = generate_chain(password, chain_length)
        table[chain[0]] = (password, chain[-1])

        for j in range(1, len(chain)):
            chain_hash = hashlib.md5(chain[j].encode('utf-8')).hexdigest()
            table[chain_hash] = (password, chain[-1])

        if i % 100 == 0:
            print(f"Generated chain {i}/{num_chains}")

    # Save table to file
    with open(filename, "w") as f:
        for k, v in table.items():
            f.write(f"{k}:{v[0]}:{v[1]}\n")

    return table

def generate_password(charset, length):
    import string

    if charset == 'lowercase':
        chars = string.ascii_lowercase
    elif charset == 'uppercase':
        chars = string.ascii_uppercase
    elif charset == 'digits':
        chars = string.digits
    elif charset == 'special':
        chars = string.punctuation
    else:
        chars = string.ascii_letters + string.digits + string.punctuation

    import random
    return ''.join(random.choice(chars) for i in range(length))

def generate_chain(password, chain_length):
    chain = [password]

    for i in range(chain_length):
        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        password = reduce_hash(password_hash)

        chain.append(password)

    return chain

def reduce_hash(hash):
    import string

    # Reduce the hash to a password
    password = ""
    for char in hash:
        if char in string.ascii_letters:
            password += char
        if len(password) == 7:
            break

    return password

if __name__ == '__main__':
    url = input("Enter the website URL to crawl: ")
    hashes = crawl_website(url)
    if len(hashes) > 0:
        print(f"Found {len(hashes)} hashes.")
        filename = input("Enter the name of the file to save the hashes: ")
        sort_hashes(hashes, filename)
        table = create_rainbow_table()
        check_hashes(filename, table)
    else:
        print("No hashes found on the website.")
