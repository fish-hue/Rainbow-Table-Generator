# Rainbow-Table-Generator
This is a work in progress. 
The goal is to be able to generate custom Rainbow Tables.
Right now my focus is on SHA1 and MD5 hashes
A SHA1 and MD5 script to check a hash against a created table for plaintext will come..

# Select hashimo-sha1.py or hashimo-md5.py and execute as follows:
python hashimo-sha1
-or-
python hashimo-md5.py
# Follow prompts to create a custom table
This will create a .txt file full of MD5 hashes and corresponging plaintext values.
There will be a prompt to enter plaintext that will be converted to MD5 for search in the created table
Results of the search will be shown.
*script can be modified to create more results or less as needed

NOT DONE YET | TO-DO:

Create a table reading script that will take a hash input
Then check the input against the data in a generated table
Finally print the plaintext value found, if any
I will make duplicate scripts, one for MD5 and one for SHA1
