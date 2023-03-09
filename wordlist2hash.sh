#!/bin/bash

echo "Wordlist to Hash Converter"

echo "Enter path to wordlist:"
read input_file

echo "Please choose a hash type (1 for SHA1, 2 for MD5):"
read hash_choice

if [[ "$hash_choice" == "1" ]]; then
    hash_type="sha1"
elif [[ "$hash_choice" == "2" ]]; then
    hash_type="md5"
else
    echo "Invalid choice."
    exit 1
fi

echo "Enter the name of the output file:"
read output_file

while read -r line; do
    hash=$(echo -n "$line" | openssl "$hash_type" | awk '{print $2}')
    echo "$line:$hash" >> "$output_file"
done < "$input_file"

echo "Hashes generated and saved to $output_file."
