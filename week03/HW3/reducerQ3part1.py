#!/usr/bin/env python

from collections import defaultdict
import sys

def main(separator='\t'):
    total = 0
    unique_items = 0
    largest_basket = 0
    current_item = None
    current_count = 0
    
    # input comes from STDIN (standard input)
    for line in sys.stdin:
        item, count, basketsize = line.split(separator)
        if item == '*':
            total += int(count.strip())
            sys.stderr.write("reporter:counter:Code Call Counters,Recieved Totals,1\n")
        else:
            # still counting the same key, keep accumulating
            if current_item == item.strip():
                current_count += int(count.strip())
            else:
                if current_item:
                    # emit the accumulated key count
                    sys.stdout.write("{0}{1}{2}\n".format(current_item, separator, current_count))

                # set/reset state
                current_count = int(count.strip())
                current_item = item.strip()
                largest_basket = max(largest_basket, int(basketsize.strip()))
                # increment the unique item count
                unique_items += 1
                # increment the unique item counter
                sys.stderr.write("reporter:counter:Code Call Counters,Unique Item Counter,1\n")

    if current_item:
            # emit the last accumulated key count
            sys.stdout.write("{0}{1}{2}\n".format(current_item, separator, current_count))
    
    # emit special key for max basket size
    sys.stdout.write("{0}{1}{2}\n".format('*MAXBASKET', separator, largest_basket))
    
    # emit special key for max basket size
    sys.stdout.write("{0}{1}{2}\n".format('*UNIQUEITEMS', separator, unique_items))
    
    #emit special key for total items
    sys.stdout.write("{0}{1}{2}\n".format('*TOTALITEMS', separator, total))    
    
if __name__ == "__main__":
    # increment counter for combiner call, write to STDERR
    sys.stderr.write("reporter:counter:Code Call Counters,reducer,1\n")
    main()