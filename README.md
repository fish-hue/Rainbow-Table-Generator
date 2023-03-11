# Welcome to hash-tools.sh
This is a work in progress. 
The goal is to be able to gather Hashes, generate custom Rainbow Tables, then search them with the hashes collected to see if a password can be found.
Right now my focus is on SHA1 and MD5 hashes
There are serveral tools to please read below

# Use RainbowKingMD5.py All in One Hash Collector, Table Generator, and Cracker for MD5 hashes
python RainbowKingMD5.py

# Only Collect hashes using hash-collector.py
python hash-collector.py

This will search a URL for all hashes in any format and display them with the option to save as a file

# Only Create a Rainbow Table using Hashimo
Select hashimo-sha1.py or hashimo-md5.py and execute as follows:

Type: python hashimo-sha1

-or-

Type: python hashimo-md5.py
# Follow prompts to generate a custom table
This will create a .txt file full of MD5 hashes and corresponging plaintext values.
There will be a prompt to enter plaintext that will be converted to MD5 for search in the created table
Results of the search will be shown.
The script can be modified to create more results or less as needed

# Use wordlist2hash.sh to covert wordlist to SHA1 or MD5

Type: chmod +x wordlist2hash.sh

Then run: ./wordlist2hash.sh

Follow instructions and choose a MD5 or SHA1 hash as well as a filename. 
This script will generate a new wordlist that includes a line by line hash:plaintext format

# Use htcheck.sh to search for plaintext passwords in the generated table
Type: chmod +x htcheck.sh

Then run: ./htcheck.sh

This will then prompt the user to provide a file to use as the Rainbow Table
With another prompt for the user to provide the hash data.
Successfull results will be shown as plaintext. This script is very basic and sill not work with other rainbow tables, only the ones made using hashimo-sha1.py or hashimo-md5.py


