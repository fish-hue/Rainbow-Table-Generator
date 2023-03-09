#!/bin/bash

# Prompt user for input file
echo "Please enter the path to the input file:"
read input_file

# Prompt user to choose hash type
echo "Please choose a hash type (1 for SHA1, 2 for MD5):"
read hash_choice

# Set hash type based on user input
if [[ "$hash_choice" == "1" ]]; then
    hash_type="sha1"
elif [[ "$hash_choice" == "2" ]]; then
    hash_type="md5"
else
    echo "Invalid hash type choice."
    exit 1
fi

# Prompt user for output file name
echo "Please enter the name of the output file:"
read output_file

# Loop through input file and generate hashes
while read -r line; do
    hash=$(echo -n "$line" | openssl "$hash_type" | awk '{print $2}')
    echo "$hash:$line" >> "$output_file"
done < "$input_file"

echo "Hashes generated and saved to $output_file."
