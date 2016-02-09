#!/usr/bin/env python

import sys

total_items = 1.0
unique_items = 0
max_basket = 0

def main(separator='\t'):    
    # input comes from STDIN (standard input)
    for line in (sys.stdin):
        item, count = line.strip().split(separator)
        
        # these special keys should arrive first
        if item.strip() == '*TOTALITEMS':
            total_items = float(count.strip())
        elif item.strip() == '*UNIQUEITEMS':
            unique_items = int(count.strip())
        elif item.strip() == '*MAXBASKET':
            max_basket = int(count.strip())
        else:    
            sys.stdout.write('{0}{1}{2}{1}{3}\n'.format(item, separator, count, float(count)/total_items))
        
if __name__ == "__main__":
    # increment counter for combiner call, write to STDERR
    sys.stderr.write("reporter:counter:Code Call Counters,reducer,1\n")
    main()