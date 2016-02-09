#!/usr/bin/env python

import sys

def main(separator='\t'):
    largest_basket = 0
    current_item = None
    current_count = 0
    
    # input comes from STDIN (standard input)
    for line in sys.stdin:
        # read a line and split into item, count, and basketsize
        item, count, basketsize = line.split(separator)

        # still counting the same key, keep accumulating
        if current_item == item.strip():
            current_count += int(count.strip())
        else:
            if current_item:
                # emit the accumulated key count
                sys.stdout.write("{0}{1}{2}{1}{3}\n".format(current_item, separator, current_count, largest_basket))

            # set/reset state
            current_count = int(count.strip())
            current_item = item.strip()
            largest_basket = max(largest_basket, int(basketsize.strip()))

    if current_item:
        # emit the last accumulated key count
        sys.stdout.write("{0}{1}{2}{1}{3}\n".format(current_item, separator, current_count, largest_basket))

    
if __name__ == "__main__":
    # increment counter for combiner call, write to STDERR
    sys.stderr.write("reporter:counter:Code Call Counters,combiner,1\n")
    main()