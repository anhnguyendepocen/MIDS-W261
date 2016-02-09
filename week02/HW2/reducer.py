#!/usr/bin/python
## reducer.py
## Author: Ron Cordell
## Description: reducer code for HW2.2
## given a list of key,value pairs for word, count, aggregate and output the list
from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None
all_words = []

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)

    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # append result to list
            all_words.append((current_word, current_count))
        current_count = count
        current_word = word

# do not forget to output the last word if needed!
if current_word == word:
    all_words.append((current_word, current_count))
    
# sort the list by value
sorted_words = sorted(all_words, key=lambda pair: pair[1], reverse=True)

# write out the top 10
for i,word in enumerate(sorted_words):
    print '{0}\t{1}'.format(word[0],word[1])
    if i >= 10:
        break