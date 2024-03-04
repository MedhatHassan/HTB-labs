import re

# Open and read the text file
file_path = 'nmap.txt'
with open(file_path, 'r') as file:
    text = file.read()

# Define the regular expression pattern
pattern = r'\S+\.\S+\.\S+4'

# Find all matches in the text
matches = re.findall(pattern, text)

# Print the matches
for match in matches:
    print(match)
