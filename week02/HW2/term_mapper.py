#!/usr/bin/python
## mapper.py
## Author: Ron Cordell
## Description: mapper code for HW2.3
## Given input on STDIN read lines and count occurrences of words
## Output a key, value => (token, email id, class, term_flag) = count

import sys
import re

## Lines in the file have 4 fields:
## ID \t SPAM \t SUBJECT \t CONTENT \n
WORD_RE = re.compile(r"[\w']+")

all_words = False
## Words in the word list are space delimited
## If no words specified, use all tokens as vocabulary terms
if len(sys.argv) > 1:
    wordlist = sys.argv[1].lower().split(' ')
else:
    all_words = True

# read each email as a line from stdin
for line in sys.stdin:
    try:
        # Split the line into the 4 fields
        email_id, label, subject, body = line.split('\t')
    except ValueError:
        # If there are 3 fields the assume the 3rd field is the body
        email_id, label, body = line.split('\t')
        subject = ''
    
    # extract only words from the combined subject and body text
    for token in WORD_RE.findall(subject + ' ' + body):
        # term indicates that this is a vocabulary word 
        # when not all words are considered this lets downstream processors know which are which
        term = '0'
        if all_words:
            term = '1'
        elif token.lower() in wordlist:
            term = '1'
            
        # emit on each word a key, value pair of [(word, id, label, term),1]
        # so that the sort function operates on the words as keys
        print('{0}\t{1}\t{2}\t{3}\t{4}'.format(token, email_id, label, term, 1))