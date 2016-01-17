#!/usr/bin/python
import sys
import re
count = 0
WORD_RE = re.compile(r"[\w']+")
filename = sys.argv[2]
findword = sys.argv[1]
with open (filename, "r") as myfile:
    for line in myfile.readlines():
        for word in WORD_RE.findall(line):
            if word.lower() == findword.lower():
                count += 1
                break
with open ('{0}.intermediateCount'.format(filename),'w') as outfile:
    outfile.write('{0}\n'.format(count))