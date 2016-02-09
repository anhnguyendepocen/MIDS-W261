#!/usr/bin/env python
#
# W261 HW 3.1 MapReduce and Counters
#
# Read from a CSV file of consumer complaints with fields as follows:
#
# Complaint ID,Product,Sub-product,Issue,Sub-issue,State,ZIP code,Submitted via,Date received,
# Date sent to company,Company,Company response,Timely response?,Consumer disputed?
#
# Use counters to count the number of complaints for Product Id's of debt collection, mortgage,
# and everything else (3 categories)
#
# Remember that in Hadoop streaming, to update a counter is to write to STDERR in the format
# reporter:counter:<group>,<counter>,<amount>

import sys

# Read data from STDIN and use counters to count the data
def main(separator=','):
    # input comes from STDIN (standard input) as the fields from the CSV
    for line in (sys.stdin):
        fields = line.split(separator)
        try:
            # check to see if this is a header by trying to convert the first field to an integer
            id = int(fields[0])
            # we have a real record, so do some mapping
            counter_name = None
            if (fields[1].lower() == 'debt collection' or \
                fields[1].lower() == 'mortgage'):
                counter_name = fields[1].strip().lower()
            else:
                counter_name = 'other'
            # update the counter
            sys.stderr.write("reporter:counter:Category Counters,{0},1\n".format(counter_name))
        except:
            # must be a header record so skip it
            pass

            

if __name__ == "__main__":
    main()