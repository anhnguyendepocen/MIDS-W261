#!/usr/bin/env python
#
# W261 HW 3.3 MapReduce and Counters for Code Analysis
#
# Read a line of product ids where each line is a user session and the ids are products the user viewed
# Emit product_id, 1
#
# Use counters to count the number of times the mapper is called
#
# Remember that in Hadoop streaming, to update a counter is to write to STDERR in the format
# reporter:counter:<group>,<counter>,<amount>

import sys

# Read data from STDIN and use counters to count the data
def main(separator='\t'):   
    for line in sys.stdin:
        item, count = line.strip().split(separator)
        sys.stdout.write('{0}{1}{2}\n'.format(item, separator, count))
        
if __name__ == "__main__":
    # increment counter for mapper call, write to STDERR
    sys.stderr.write("reporter:counter:Code Call Counters,mapper,1\n")
    main()