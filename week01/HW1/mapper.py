#!/usr/bin/python
## mapper.py
## Author: Ron Cordell
## Description: mapper code for HW1.4
## Given a file and list of words, read lines and count occurrences of words
## Output a key, value => (id, class, token, term_flag) = count

import sys
import re

## Lines in the file have 4 fields:
## ID \t SPAM \t SUBJECT \t CONTENT \n
WORD_RE = re.compile(r"[\w']+")

filename = sys.argv[1]

## Words in the word list are space delimited
wordlist = sys.argv[2].lower().split(' ')

all_words = False
if wordlist[0] == '*':
    all_words = True
    
counts = {}

with open (filename, "rU") as myfile:
    for line in myfile.readlines():
        fields = line.split('\t')      
        if len(fields) > 3:
            # we are interested in subject and body but need to be resilient for missing fields
            text = '{0} {1}'.format(fields[2],fields[3])
        elif len(fields) > 2:
            text = fields[2]
        # extract only words from the combined subject and body text
        for word in WORD_RE.findall(text):
            term = '0'
            if all_words:
                term = '1'
            elif word.lower() in wordlist:
                term = '1'
            try:
                counts[(fields[0],fields[1],word.lower(), term)] += 1
            except:
                counts[(fields[0],fields[1],word.lower(), term)] = 1
        # ensure that all words in the list are represented even if they don't occur
        if not all_words:
            for word in wordlist:
                try:
                    if counts[(fields[0],fields[1], word, '1')] > 0:
                        pass
                except KeyError:
                    counts[(fields[0], fields[1], word, '1')] = 0

for key in counts:
    sys.stdout.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(key[0], key[1], key[2], key[3], counts[key]))