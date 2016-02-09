#!/usr/bin/env python
#
# W261 HW 3.2 MapReduce and Counters for Code Analysis
# Read from a CSV file of consumer complaints with fields as follows:
#
# Complaint ID,Product,Sub-product,Issue,Sub-issue,State,ZIP code,Submitted via,Date received,
# Date sent to company,Company,Company response,Timely response?,Consumer disputed?
#
# Use counters to count the number of times the mapper is called
#
# Remember that in Hadoop streaming, to update a counter is to write to STDERR in the format
# reporter:counter:<group>,<counter>,<amount>

import sys
import re

WORD_RE = re.compile(r"[\w']+")

# Read data from STDIN and use counters to count the data
def main(separator='\t'):   
    for line in sys.stdin:
        fields = line.split(',')
        try:
            # check to see if this is a header by trying to convert the first field to an integer
            id = int(fields[0])
            # we have a real record, so do some mapping
            for word in WORD_RE.findall(fields[3]):
                sys.stdout.write('{0}{1}{2}\n'.format(word.lower(), separator, 1))
                sys.stdout.write('{0}{1}{2}\n'.format('*',  separator, 1))
        except:
            # must be a header record so skip it
            pass

if __name__ == "__main__":
    # increment counter for mapper call, write to STDERR
    sys.stderr.write("reporter:counter:Code Call Counters,mapper,1\n")
    main()