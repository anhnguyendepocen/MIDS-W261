#!/usr/bin/python
import sys
import re
count = 0
WORD_RE = re.compile(r"[\w']+")


# the word to find is the first argument
findword = sys.argv[1].lower()

# the file to scan is the second argument
filename = sys.argv[2]

# open the file, read it line by line
with open (filename, "r") as myfile:
    for line in myfile.readlines():
        
        # process each word in the line by filtering out non-words and if it matches
        # the search word, incrementing the word count
        for word in WORD_RE.findall(line):
            # make this a case-insensitve search
            if word.lower() == findword:
                count += 1
            
# now that we've counted this line, write out the count
with open ('{0}.intermediateCount'.format(filename),'w') as outfile:
    outfile.write('{0}\n'.format(count))