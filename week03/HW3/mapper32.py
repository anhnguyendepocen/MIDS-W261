#!/usr/bin/env python
#
# W261 HW 3.2 MapReduce and Counters for Code Analysis
#
# Simple word counter
#
# Use counters to count the number of times the mapper is called
#
# Remember that in Hadoop streaming, to update a counter is to write to STDERR in the format
# reporter:counter:<group>,<counter>,<amount>

import sys

def read_input(file):
    for line in file:
        # split the line into words
        yield line.split()
        
# Read data from STDIN and use counters to count the data
def main(separator=','):    
    data = read_input(sys.stdin)
    for words in data:
        # write the results to STDOUT
        # tab-delimited; the trivial word count is 1
        for word in words:
            sys.stdout.write('{0}{1}{2}\n'.format(word, separator, 1))         

if __name__ == "__main__":
    # increment counter for mapper call, write to STDERR
    sys.stderr.write("reporter:counter:Code Call Counters,mapper,1\n")
    main()